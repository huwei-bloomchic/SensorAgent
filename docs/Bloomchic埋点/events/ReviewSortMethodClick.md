# ReviewSortMethodClick

## 基本信息

- **事件显示名**: 使用某个排序方式
- **事件英文名**: `ReviewSortMethodClick`
- **所属模块**: 3.【商详页】的埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `review_from_module` | 评论列表来源入口 | STRING | 商品价格右侧评论、[Fit]模块, 商详View All |  | 确认使用某个排序时上报 |  |  |
| `product_spu` | 商品SPU | STRING | 当前商品SPU编号 | JavaScript |  |  |  |
| `product_name` | 商品名称 | STRING |  | JavaScript |  |  |  |
| `is_available` | 可用状态 | BOOL | 仅当该商品的所有规格都无货时会触发会上报false | JavaScript |  |  |  |
| `web_original_price` | 原价 | NUMBER |  | JavaScript |  |  |  |
| `web_current_price` | 价格 | NUMBER |  | JavaScript |  |  |  |
| `web_discount_price` | 折扣 | NUMBER |  | JavaScript |  |  |  |
| `review_number` | 评价数量 | INT | 1) 通过审核的评价总数(人工审核、自动审核)：0、1、2、3...<br/>2) 当没有评价时，此时数量取0 | JavaScript |  |  |  |
| `average_overall_rating` | 综合评分均值 | NUMBER | 1) 取综合评分均值，小数点后一位：1、1.1、1.2...2.1、2.2...4.9、5<br/>2) 当评价数量为0时，此时的综合评分为0 | JavaScript |  |  |  |
| `sort_method` | 排序方式 | STRING | 上报具体使用的排序方式，比如<br/>Pictures/Videos First、Most Recent、Highest Rating、Lowest Rating | JavaScript |  |  |  |
