# add_payment_info

## 基本信息

- **事件显示名**: 点击Pay now
- **事件英文名**: `add_payment_info`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `currency` | 币种类型 | STRING |  | JavaScript | 点击Pay now 按钮时上报 |  | Checkout 升级<br/>1、PayPal暂不捕获收集不了<br/>2、如果用户不选择支付方式,payment_type是没有办法获取到的<br/>3、页面三合一,原有add_shipping_info事件不会再上传,现在与add_payment_info事件整合一起,多增加shipping_tier字段<br/>测试工具:暂无,无法连接到工具,<br/>目前在控制台打印出日志,在控制台查看网络请求,可把当前内容记录到文本,6-8小时后到平台(analytics)核验数据 |
| `value` | 总计金额 | NUMBER |  | JavaScript |  |  |  |
| `payment_type` | 支付类型 | STRING |  | STRING |  |  |  |
| `shipping_tier` | 快递方式 | STRING |  | STRING |  |  |  |
| `items[]:content_id` | 组合后的ID | STRING |  | JavaScript |  |  |  |
| `items[]:content_type` | 固定填写:product | STRING |  | JavaScript |  |  |  |
| `items[]:content_name` | 名称 | STRING |  | JavaScript |  |  |  |
| `items[]:price` | 单件价格 | NUMBER |  | JavaScript |  |  |  |
| `items[]:quantity` | 数量 | NUMBER |  | JavaScript |  |  |  |
