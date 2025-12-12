# FilterDoneClick

## 基本信息

- **事件显示名**: 点击filter弹窗的提交
- **事件英文名**: `FilterDoneClick`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `current_page` | 当前页面 | STRING | 当前页面：搜索结果页、商品列表页 |  |  |  |  |
| `collection_id` | 集合页ID | STRING |  |  |  |  |  |
| `collection_handle` | 集合页Handle | STRING |  |  |  |  |  |
| `filter_key_list` | 筛选项key | STRING | 数组，多个筛选项key一起提交,<br/>示例：filter.p.m.Product.development_flower,filter.p.product_type.sweatshirts |  |  |  |  |
| `text_list` | 选项文本 | STRING | 数组，多个筛选项一起提交<br/>示例：Maxi Dresses,Swim Tops,Sleeve type |  |  |  |  |
