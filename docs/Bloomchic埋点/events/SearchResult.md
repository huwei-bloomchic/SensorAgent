# SearchResult

## 基本信息

- **事件显示名**: SearchResult 返回搜索结果时上报<br/>有搜索到内容就上报true，否则是false，<br/>有筛选条件时不上报，同fb上报逻辑，<br/>异常时不上报
- **事件英文名**: `SearchResult`
- **所属模块**: 0.全局埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `search_content` | 搜索的内容 | STRING |  |  |  |  |  |
| `search_success` | 搜索的结果， | BOOLEAN |  |  |  |  |  |
| `product_id_list` | Shopify Product ID集合 | STRING | 搜索结果第一页商品集合，搜索列表的producti_id集合，web端一般有40个，客户端有10个。翻页不重复上报。搜索结果为空时不上报。 |  |  |  |  |
| `product_spu_list` | 商品SPU列表 | STRING | 搜索结果第一页商品集合，搜索列表的spu_id集合，web端一般有40个，客户端有10个。翻页不重复上报。搜索结果为空时不上报。 |  |  |  |  |
