# 렛츠에셋 (Let's Asset) — 글로벌 다국적 기업·공시·증권 인텔리전스 독립 원장

> 금융감독원 DART의 모든 상장사 15개년 재무·임원·감사의견·지분변동과 미국(SEC EDGAR 6,850개사), 중국(CSI 300), 일본(Nikkei 225), 러시아(MOEX 50) 등 글로벌 주요 강대국 상장사의 모든 데이터를 수집·분석·관리하는 독립 증권·자산 데이터 원장입니다.
> 증권을 기반으로 한 전 세계 기업의 역사, 재무 건전성, 임원 지배구조 및 거시 매크로 자산 흐름을 한곳에서 살펴보고 통제하는 독립 플랫폼을 지향합니다.

---

## 1. 글로벌 온톨로지 식별자 체계 (Global Federated URN)
- **국내 기업 식별자**: `urn:asset:corp:kr:{종목코드}` (예: `urn:asset:corp:kr:005930`, `urn:asset:corp:kr:000660`)
- **미국 상장사 식별자**: `urn:asset:corp:us:{티커}` (예: `urn:asset:corp:us:NVDA`, `urn:asset:corp:us:AAPL`)
- **글로벌 다국적 기업**: `urn:asset:corp:cn:{종목코드}`, `urn:asset:corp:jp:{종목코드}`, `urn:asset:corp:ru:{종목코드}`
- **기업 등기/미등기 임원 연동**: `urn:people:person:{p_id}` (렛츠피플 레포지토리와 상호 연계)

---

## 2. 제공 엔드포인트 및 데이터 정본
- **미국 SEC 6,850사 색인**: `data/sec_tickers_index.json`
- **DART 전방위 인텔리전스 (재무·임원·감사·제재)**: `data/all_dimensions_dossier.json`
- **글로벌 4대 강대국 상장사 원장**: `data/global_expansion_dossier.json`
- **글로벌 자산 관제 웹 대시보드**: `index.html`
- **글로벌 수집 및 90% 승격 엔진**: `scripts/crawler.py`

## 3. 서비스 간 데이터 연동 방식 (뉴스보드 및 타 서비스)
```javascript
// 외부 서비스에서 렛츠에셋 기업·주식 데이터 연동 예시
async function loadLetAssetCorp(stockCode) {
  const url = `https://pyw31337.github.io/asset/data/all_dimensions_dossier.json`;
  const localFallback = `../asset/data/all_dimensions_dossier.json`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    return data.companies?.[stockCode];
  } catch (e) {
    const fallbackRes = await fetch(localFallback);
    const data = await fallbackRes.json();
    return data.companies?.[stockCode];
  }
}
```
