# CollectionTurnPage

## 基本信息

- **事件显示名**: 点击翻页
- **事件英文名**: `CollectionTurnPage`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `collection_id` | 列表ID | STRING |  | JavaScript | 每次点击某一页或点击>均上报 |  |  |
| `collection_name` | 列表名称 | STRING |  | JavaScript |  |  |  |
| `turn_page_type` | 翻页类型 | STRING | 1=自动加载下一页<br/>2=手动点击翻页 | JavaScript |  | 9.1后才有上报 |  |
