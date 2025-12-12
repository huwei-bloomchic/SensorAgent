# DeleteMyFilter

## 基本信息

- **事件显示名**: 删除【我的Filter】
- **事件英文名**: `DeleteMyFilter`
- **所属模块**: 2.【商品】相关埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `filter_key_list` | 筛选项key | STRING | 全选我的filter时，选项list<br/>数组，多个筛选项key一起提交,<br/>示例：filter.p.m.Product.development_flower,filter.p.product_type.sweatshirts |  |  |  |  |
| `text_list` | 选项文本 | STRING | 全选我的filter时，选项list<br/>数组，多个筛选项key一起提交,<br/>示例：filter.p.m.Product.development_flower,filter.p.product_type.sweatshirts |  |  |  |  |
