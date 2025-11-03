"""
Streamlit Web Application for Clinical Document Review
웹 브라우저에서 문서를 업로드하고 검토 결과를 확인할 수 있습니다.

실행 방법:
    pip install streamlit
    streamlit run web_app.py
"""

import streamlit as st
import sys
from pathlib import Path
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from parsers import PDFParser
from reviewers import ProtocolReviewer, IBReviewer, SAPReviewer
from reports import HTMLReportGenerator, TextReportGenerator


# Page config
st.set_page_config(
    page_title="임상문서 자동 검토 도구",
    page_icon="📋",
    layout="wide"
)

# Title
st.title("📋 임상문서 자동 검토 도구")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("ℹ️ 정보")
    st.info("""
    **완전 로컬 처리**

    업로드된 문서는 서버 메모리에서만 처리되며
    외부로 전송되지 않습니다.

    검토 완료 후 자동으로 삭제됩니다.
    """)

    st.header("📚 지원 문서")
    st.markdown("""
    - **Protocol**: 임상시험 계획서
    - **IB**: 임상시험자 자료집
    - **SAP**: 통계분석계획서
    """)

    st.header("🔒 보안")
    st.success("""
    ✅ 로컬 서버에서만 실행

    ✅ 외부 전송 없음

    ✅ 세션 종료 시 자동 삭제
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("1️⃣ 문서 업로드")
    uploaded_file = st.file_uploader(
        "PDF 파일을 선택하세요",
        type=['pdf'],
        help="프로토콜, IB, 또는 SAP PDF 문서를 업로드하세요"
    )

with col2:
    st.header("2️⃣ 문서 타입 선택")
    doc_type = st.selectbox(
        "문서 타입",
        ["Protocol", "IB", "SAP"],
        help="검토할 문서의 타입을 선택하세요"
    )

st.markdown("---")

# Process button
if uploaded_file is not None:
    st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")

    # File info
    file_size = uploaded_file.size / 1024  # KB
    st.info(f"📄 파일 크기: {file_size:.2f} KB")

    # Review button
    if st.button("🔍 검토 시작", type="primary", use_container_width=True):

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Save uploaded file temporarily
            status_text.text("⏳ 파일 처리 중...")
            progress_bar.progress(20)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Step 2: Parse document
            status_text.text("⏳ 문서 파싱 중...")
            progress_bar.progress(40)

            parser = PDFParser(tmp_path)
            parsed_doc = parser.parse()

            # Step 3: Review document
            status_text.text("⏳ 문서 검토 중...")
            progress_bar.progress(60)

            reviewers = {
                'Protocol': ProtocolReviewer,
                'IB': IBReviewer,
                'SAP': SAPReviewer
            }

            reviewer = reviewers[doc_type]()
            review_results = reviewer.review_document(parsed_doc)

            # Step 4: Generate report
            status_text.text("⏳ 보고서 생성 중...")
            progress_bar.progress(80)

            html_gen = HTMLReportGenerator()
            html_report = html_gen.generate(review_results)

            text_gen = TextReportGenerator()
            text_report = text_gen.generate(review_results)

            progress_bar.progress(100)
            status_text.text("✅ 검토 완료!")

            # Clean up temp file
            os.unlink(tmp_path)

            # Display results
            st.markdown("---")
            st.header("📊 검토 결과")

            summary = review_results['summary']

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("전체 검토 항목", summary['total_checks'])

            with col2:
                st.metric("통과", summary['passed'],
                         delta=f"{summary['pass_rate']:.1f}%")

            with col3:
                st.metric("실패", summary['failed'],
                         delta=f"-{100-summary['pass_rate']:.1f}%",
                         delta_color="inverse")

            with col4:
                st.metric("통과율", f"{summary['pass_rate']:.1f}%")

            # Issues by severity
            st.subheader("⚠️ 중요도별 이슈")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.error(f"**Critical**: {summary['critical_issues']}개")

            with col2:
                st.warning(f"**Major**: {summary['major_issues']}개")

            with col3:
                st.info(f"**Minor**: {summary['minor_issues']}개")

            st.markdown("---")

            # Detailed findings
            st.subheader("📋 상세 검토 결과")

            for section_data in review_results['findings']:
                with st.expander(f"📂 {section_data['section']}"):
                    checks = section_data['checks']

                    passed_checks = [c for c in checks if c['passed']]
                    failed_checks = [c for c in checks if not c['passed']]

                    st.write(f"**통과**: {len(passed_checks)}/{len(checks)}")

                    if failed_checks:
                        st.error(f"**실패한 항목**: {len(failed_checks)}개")

                        for check in failed_checks:
                            severity_emoji = {
                                'critical': '🔴',
                                'major': '🟡',
                                'minor': '🔵'
                            }[check['severity']]

                            st.markdown(f"""
                            {severity_emoji} **{check['id']}** - {check['category']}
                            - {check['description']}
                            - 누락된 키워드: `{', '.join(check['missing_keywords'])}`
                            """)
                    else:
                        st.success("✅ 모든 항목 통과")

            st.markdown("---")

            # Download buttons
            st.subheader("💾 보고서 다운로드")

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📄 HTML 보고서 다운로드",
                    data=html_report,
                    file_name=f"{Path(uploaded_file.name).stem}_report.html",
                    mime="text/html",
                    use_container_width=True
                )

            with col2:
                st.download_button(
                    label="📝 텍스트 보고서 다운로드",
                    data=text_report,
                    file_name=f"{Path(uploaded_file.name).stem}_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ 오류 발생: {str(e)}")
            import traceback
            with st.expander("상세 오류 정보"):
                st.code(traceback.format_exc())

            # Clean up on error
            if 'tmp_path' in locals():
                try:
                    os.unlink(tmp_path)
                except:
                    pass

else:
    st.info("👆 PDF 파일을 업로드하여 시작하세요")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>임상문서 자동 검토 도구 v1.0.0</p>
    <p>⚠️ 이 도구는 검토를 보조하는 도구입니다. 최종 검토 및 승인은 담당 전문가가 수행해야 합니다.</p>
</div>
""", unsafe_allow_html=True)
