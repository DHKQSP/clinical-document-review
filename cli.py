#!/usr/bin/env python3
"""
Clinical Document Review Tool - CLI
로컬에서 실행되는 임상문서 자동 검토 도구
"""

import click
import sys
from pathlib import Path
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from parsers import PDFParser
from reviewers import ProtocolReviewer, IBReviewer, SAPReviewer
from reports import HTMLReportGenerator, TextReportGenerator


# Document type mapping
REVIEWERS = {
    'protocol': ProtocolReviewer,
    'ib': IBReviewer,
    'sap': SAPReviewer
}


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    임상문서 자동 검토 도구

    프로토콜, IB, SAP 문서를 로컬에서 안전하게 검토합니다.
    문서는 외부로 전송되지 않으며 모든 처리가 로컬에서 이루어집니다.
    """
    pass


@cli.command()
@click.argument('document_path', type=click.Path(exists=True))
@click.option('--type', '-t', 'doc_type',
              type=click.Choice(['protocol', 'ib', 'sap'], case_sensitive=False),
              required=True,
              help='문서 타입 (protocol/ib/sap)')
@click.option('--output', '-o', 'output_path',
              type=click.Path(),
              help='출력 파일 경로 (기본: reports/<filename>_report.html)')
@click.option('--format', '-f', 'output_format',
              type=click.Choice(['html', 'text', 'both'], case_sensitive=False),
              default='html',
              help='보고서 형식 (기본: html)')
def review(document_path, doc_type, output_path, output_format):
    """
    문서를 검토하고 보고서를 생성합니다.

    예시:
        cli.py review protocol.pdf --type protocol
        cli.py review ib.pdf --type ib --format both
        cli.py review sap.pdf --type sap --output my_report.html
    """
    try:
        click.echo(f"\n{Fore.CYAN}{'='*60}")
        click.echo(f"{Fore.CYAN}임상문서 자동 검토 도구")
        click.echo(f"{Fore.CYAN}{'='*60}\n")

        # Step 1: Parse document
        click.echo(f"{Fore.YELLOW}[1/3] 문서 파싱 중...")
        parser = PDFParser(document_path)

        with tqdm(total=100, desc="파싱 진행", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            parsed_doc = parser.parse()
            pbar.update(100)

        click.echo(f"{Fore.GREEN}✓ 파싱 완료: {parsed_doc['page_count']}페이지\n")

        # Step 2: Review document
        click.echo(f"{Fore.YELLOW}[2/3] 문서 검토 중...")
        reviewer_class = REVIEWERS[doc_type.lower()]
        reviewer = reviewer_class()

        with tqdm(total=100, desc="검토 진행", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            review_results = reviewer.review_document(parsed_doc)
            pbar.update(100)

        # Display summary
        summary = review_results['summary']
        click.echo(f"\n{Fore.GREEN}✓ 검토 완료")
        click.echo(f"  - 전체 검토 항목: {summary['total_checks']}")
        click.echo(f"  - 통과: {Fore.GREEN}{summary['passed']}{Style.RESET_ALL}")
        click.echo(f"  - 실패: {Fore.RED}{summary['failed']}{Style.RESET_ALL}")
        click.echo(f"  - 통과율: {summary['pass_rate']:.1f}%")

        # Show critical issues
        if summary['critical_issues'] > 0:
            click.echo(f"\n  {Fore.RED}⚠ Critical 이슈: {summary['critical_issues']}개")
        if summary['major_issues'] > 0:
            click.echo(f"  {Fore.YELLOW}⚠ Major 이슈: {summary['major_issues']}개")
        if summary['minor_issues'] > 0:
            click.echo(f"  {Fore.BLUE}ℹ Minor 이슈: {summary['minor_issues']}개")

        click.echo()

        # Step 3: Generate report
        click.echo(f"{Fore.YELLOW}[3/3] 보고서 생성 중...")

        # Determine output path
        if not output_path:
            reports_dir = Path('reports')
            reports_dir.mkdir(exist_ok=True)
            base_name = Path(document_path).stem
            output_path = reports_dir / f"{base_name}_report"

        output_path = Path(output_path)

        # Generate reports
        generated_files = []

        if output_format in ['html', 'both']:
            html_gen = HTMLReportGenerator()
            html_path = output_path.with_suffix('.html')
            html_gen.generate(review_results, str(html_path))
            generated_files.append(html_path)
            click.echo(f"{Fore.GREEN}✓ HTML 보고서: {html_path}")

        if output_format in ['text', 'both']:
            text_gen = TextReportGenerator()
            text_path = output_path.with_suffix('.txt')
            text_gen.generate(review_results, str(text_path))
            generated_files.append(text_path)
            click.echo(f"{Fore.GREEN}✓ 텍스트 보고서: {text_path}")

        click.echo(f"\n{Fore.CYAN}{'='*60}")
        click.echo(f"{Fore.GREEN}검토 완료!")
        click.echo(f"{Fore.CYAN}{'='*60}\n")

        # Return status based on critical issues
        if summary['critical_issues'] > 0:
            sys.exit(1)

    except FileNotFoundError as e:
        click.echo(f"\n{Fore.RED}❌ 오류: 파일을 찾을 수 없습니다 - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\n{Fore.RED}❌ 오류 발생: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('document_path', type=click.Path(exists=True))
@click.option('--pattern', '-p', help='검색할 정규표현식 패턴')
def search(document_path, pattern):
    """
    문서에서 특정 패턴을 검색합니다.

    예시:
        cli.py search protocol.pdf --pattern "version.*\\d+"
    """
    try:
        parser = PDFParser(document_path)

        if pattern:
            click.echo(f"\n{Fore.CYAN}패턴 검색 중: {pattern}\n")
            matches = parser.search_text(pattern)

            if matches:
                click.echo(f"{Fore.GREEN}✓ {len(matches)}개 발견\n")
                for i, match in enumerate(matches, 1):
                    click.echo(f"{Fore.YELLOW}[{i}] 페이지 {match['page']}:")
                    click.echo(f"  {match['match']}")
                    click.echo(f"  컨텍스트: ...{match['context']}...\n")
            else:
                click.echo(f"{Fore.RED}❌ 일치하는 항목을 찾지 못했습니다.")
        else:
            click.echo(f"{Fore.RED}❌ --pattern 옵션이 필요합니다.", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"\n{Fore.RED}❌ 오류: {e}", err=True)
        sys.exit(1)


@cli.command()
def list_checks():
    """
    사용 가능한 모든 검토 항목을 나열합니다.
    """
    click.echo(f"\n{Fore.CYAN}{'='*60}")
    click.echo(f"{Fore.CYAN}검토 항목 목록")
    click.echo(f"{Fore.CYAN}{'='*60}\n")

    for doc_type, reviewer_class in REVIEWERS.items():
        reviewer = reviewer_class()
        checklist = reviewer.checklist

        click.echo(f"\n{Fore.YELLOW}▶ {checklist['document_type']}")
        click.echo(f"{Fore.YELLOW}{'─'*60}")

        for section_key, section_data in checklist['sections'].items():
            click.echo(f"\n  {Fore.CYAN}{section_data['name']}")

            for check in section_data['checks']:
                severity_color = {
                    'critical': Fore.RED,
                    'major': Fore.YELLOW,
                    'minor': Fore.BLUE
                }[check['severity']]

                click.echo(f"    {severity_color}[{check['severity'].upper()}] {check['id']}")
                click.echo(f"    {check['description']}")
                click.echo()


@cli.command()
@click.argument('document_path', type=click.Path(exists=True))
def info(document_path):
    """
    문서의 기본 정보를 표시합니다.
    """
    try:
        parser = PDFParser(document_path)
        parsed_doc = parser.parse()

        click.echo(f"\n{Fore.CYAN}{'='*60}")
        click.echo(f"{Fore.CYAN}문서 정보")
        click.echo(f"{Fore.CYAN}{'='*60}\n")

        # File info
        file_info = parsed_doc['file_info']
        click.echo(f"{Fore.YELLOW}파일 정보:")
        click.echo(f"  파일명: {file_info['filename']}")
        click.echo(f"  크기: {file_info['size_bytes']:,} bytes")
        click.echo(f"  경로: {file_info['path']}")

        # Metadata
        metadata = parsed_doc['metadata']
        click.echo(f"\n{Fore.YELLOW}메타데이터:")
        click.echo(f"  페이지 수: {metadata['num_pages']}")
        if metadata.get('title'):
            click.echo(f"  제목: {metadata['title']}")
        if metadata.get('author'):
            click.echo(f"  작성자: {metadata['author']}")

        # Sections
        sections = parsed_doc['sections']
        click.echo(f"\n{Fore.YELLOW}발견된 섹션: {len(sections)}개")
        for i, section_name in enumerate(list(sections.keys())[:10], 1):
            click.echo(f"  {i}. {section_name}")

        if len(sections) > 10:
            click.echo(f"  ... (총 {len(sections)}개)")

        click.echo()

    except Exception as e:
        click.echo(f"\n{Fore.RED}❌ 오류: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
