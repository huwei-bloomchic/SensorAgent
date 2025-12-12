# CheckoutPageClick

## 基本信息

- **事件显示名**: 勾选订阅【Email me with news and offers】
- **事件英文名**: `CheckoutPageClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `click_id` | 点击标识 | STRING | contact_marketing_opt_in | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_value` | 选中值 | STRING | true / false | JavaScript |  |  |  |
| `click_value` | 选中值 | STRING | 支付方式选中值<br/>paypal_express<br/>afterpay<br/>pay securely with checkout.com<br/>... | JavaScript |  |  |  |
| `click_id` | 点击标识 | STRING | delivery_save_shipping_information | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_value` | 选中值 | STRING | true / false | JavaScript |  |  |  |
| `click_id` | 点击标识 | STRING | delivery_sms_marketing_opt_in | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_value` | 选中值 | STRING | true / false | JavaScript |  |  |  |
| `click_id` | 点击标识 | STRING | footer_refund_policy | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_id` | 点击标识 | STRING | footer_terms_of_service | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_id` | 点击标识 | STRING | payment_billing_address_selector | JavaScript | 点击触发 |  | Checkout 升级 |
| `click_value` | 选中值 | STRING | 选中值<br/>shipping_address<br/>custom_billing_address | JavaScript |  |  |  |
