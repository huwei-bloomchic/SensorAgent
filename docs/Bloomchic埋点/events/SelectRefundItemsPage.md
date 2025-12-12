# SelectRefundItemsPage

## 基本信息

- **事件显示名**: 选择退货商品页面曝光
- **事件英文名**: `SelectRefundItemsPage`
- **所属模块**: 6.【退货退款】埋点
- **应埋点平台**: Android,web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `email` | 用户邮箱 |  |  |  |  |  |  |
| `order` | 订单短码 |  |  |  |  |  |  |
| `refund_form` | 页面来源(0-web底部、1-个人页icon入口、2-订单详情按钮、4-其他访问) |  |  |  |  |  |  |
| `refund_product_spus` | 展示可退的商品编码/sku编码/商品id<br/>(sku,sku) |  |  |  |  |  |  |
| `refund_product_skus` |  |  |  |  |  |  |  |
| `refund_product_ids` |  |  |  |  |  |  |  |
| `no_refund_product_spus` | 展示不可退的商品编码/sku编码/商品id<br/>(sku,sku) |  |  |  |  |  |  |
| `no_refund_product_skus` |  |  |  |  |  |  |  |
| `no_refund_product_ids` |  |  |  |  |  |  |  |
| `cdp_tag_type_id` | 主标签ID |  |  |  |  |  |  |
| `cdp_tag_value_id` | 子标签ID |  |  |  |  |  |  |
| `no_refund_status_types` | /**<br/>* 产品退款状态，1; // 后台配置不可退货<br/>* 2; // 没有签收<br/>* 3; // 这个商品可以退<br/>* 4; // 商品已被退回<br/>* 5; // 商品已过退货期<br/>*/ |  |  |  |  |  |  |
