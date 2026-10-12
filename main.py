"""나만의 프롬프트 관리 - 콘솔 프로그램"""

import json
from pathlib import Path

DATA_FILE = Path("data.json")
EXPORT_DIR = Path("exports")

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 기본 프롬프트 데이터 (이전 미션에서 작성한 프롬프트로 교체해서 사용하세요)
prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요. 서론, 본론, 결론 구조를 갖추고, 독자의 관심을 끄는 제목을 3개 제안해주세요.",
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "제품 썸네일 생성",
        "content": "다음 제품의 매력적인 썸네일 이미지를 생성해주세요. 밝은 배경, 제품 중심 구도, 상단에 짧은 문구 공간을 확보해주세요.",
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": "당신은 15년 경력의 IT 컨설턴트입니다. 비전문가도 이해할 수 있게 쉬운 비유로 설명하고, 항상 장단점과 권장안을 함께 제시해주세요.",
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "뉴스 요약 프롬프트",
        "content": "다음 뉴스 기사를 3줄로 요약하고, 핵심 키워드 5개와 독자가 취할 행동 1가지를 정리해주세요.",
        "category": "자동화",
        "favorite": False,
    },
]


def get_input(message):
    """빈 값이 아닐 때까지 다시 입력받는다."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("값을 입력해주세요.")


def get_number(message, max_number):
    """1~max_number 범위의 정수를 입력받는다. 잘못되면 None을 반환한다."""
    value = input(message).strip()
    if not value.isdigit() or not 1 <= int(value) <= max_number:
        print("잘못된 번호입니다.")
        return None
    return int(value)


def select_category():
    """카테고리 목록에서 선택하거나 직접 입력한다. 취소하면 None."""
    print("카테고리 선택:")
    for i, name in enumerate(CATEGORIES, 1):
        print(f"{i}) {name}")
    value = get_input("선택 (번호 또는 직접 입력): ")
    if value.isdigit():
        if 1 <= int(value) <= len(CATEGORIES):
            return CATEGORIES[int(value) - 1]
        print("잘못된 번호입니다.")
        return None
    return value


def add_prompt():
    print("\n=== 프롬프트 추가 ===")
    title = get_input("제목: ")
    content = get_input("내용: ")
    category = None
    while category is None:
        category = select_category()
    prompts.append(
        {"title": title, "content": content, "category": category, "favorite": False}
    )
    print("프롬프트가 추가되었습니다!")


def format_line(number, prompt):
    star = " ⭐" if prompt["favorite"] else ""
    return f"{number}. [{prompt['category']}] {prompt['title']}{star}"


def print_prompts(items):
    for i, prompt in enumerate(items, 1):
        print(format_line(i, prompt))


def show_list():
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    print_prompts(prompts)
    print(f"\n총 {len(prompts)}개의 프롬프트")


def show_by_category():
    print("\n=== 카테고리별 조회 ===")
    for i, name in enumerate(CATEGORIES, 1):
        print(f"{i}) {name}")
    number = get_number("선택: ", len(CATEGORIES))
    if number is None:
        return
    category = CATEGORIES[number - 1]
    found = [p for p in prompts if p["category"] == category]
    if not found:
        print(f"[{category}] 카테고리에 등록된 프롬프트가 없습니다.")
        return
    print(f"\n[{category}] 카테고리 프롬프트:")
    print_prompts(found)
    print(f"\n총 {len(found)}개의 프롬프트")


def search_prompt():
    print("\n=== 프롬프트 검색 ===")
    keyword = get_input("검색어: ").lower()
    found = [
        p for p in prompts
        if keyword in p["title"].lower() or keyword in p["content"].lower()
    ]
    if not found:
        print("검색 결과가 없습니다.")
        return
    print("\n검색 결과:")
    print_prompts(found)
    print(f"\n{len(found)}개의 프롬프트를 찾았습니다.")


def show_detail():
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    number = get_number("번호 입력: ", len(prompts))
    if number is None:
        return
    prompt = prompts[number - 1]
    line = "─" * 28
    print(f"\n{line}")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'⭐' if prompt['favorite'] else '-'}")
    print(line)
    print("내용:")
    print(prompt["content"])
    print(line)


def toggle_favorite():
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
    print_prompts(prompts)
    number = get_number("프롬프트 번호 입력: ", len(prompts))
    if number is None:
        return
    prompt = prompts[number - 1]
    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")


def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")
    found = [p for p in prompts if p["favorite"]]
    if not found:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return
    print_prompts(found)
    print(f"\n총 {len(found)}개의 즐겨찾기")


def save_json():
    DATA_FILE.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(prompts)}개의 프롬프트를 {DATA_FILE}에 저장했습니다.")


def load_json():
    if not DATA_FILE.exists():
        print(f"{DATA_FILE} 파일이 없습니다. 먼저 저장해주세요.")
        return
    try:
        loaded = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("JSON 파일 형식이 올바르지 않습니다.")
        return
    prompts.clear()
    prompts.extend(loaded)
    print(f"{len(prompts)}개의 프롬프트를 불러왔습니다.")


def export_markdown():
    """카테고리별로 exports/<카테고리>.md 파일을 만든다."""
    if not prompts:
        print("내보낼 프롬프트가 없습니다.")
        return
    EXPORT_DIR.mkdir(exist_ok=True)
    grouped = {}
    for p in prompts:
        grouped.setdefault(p["category"], []).append(p)
    for category, items in grouped.items():
        lines = [f"# {category}", ""]
        for p in items:
            star = " ⭐" if p["favorite"] else ""
            lines += [f"## {p['title']}{star}", "", p["content"], ""]
        filename = category.replace("/", "_").replace("\\", "_") + ".md"
        (EXPORT_DIR / filename).write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(grouped)}개의 Markdown 파일을 {EXPORT_DIR}/ 에 내보냈습니다.")


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. JSON 저장")
    print("9. JSON 불러오기")
    print("10. Markdown 내보내기")
    print("0. 종료")


def main():
    while True:
        show_menu()
        choice = input("선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            save_json()
        elif choice == "9":
            load_json()
        elif choice == "10":
            export_markdown()
        else:
            print("잘못된 입력입니다. 메뉴에 있는의 번호를 입력하세요.")


if __name__ == "__main__":
    main()
