# ActivityPopupShow

## 基本信息

- **事件显示名**: 活动弹窗展示<br/>（包含浏览未购和老客复购）
- **事件英文名**: `ActivityPopupShow`
- **所属模块**: 9.【活动】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、thankyou页、me页、其他 |  |  |  |  |
| `popup_from` | 弹窗来源 | STRING | 活动触发、用户点击 【 loop_tigger, click_tigger 】 |  |  |  |  |
| `activity_id` | 活动id | STRING |  |  |  |  |  |
| `activity_name` | 活动名 | STRING |  |  |  |  |  |
| `scene_id` | 场景id | STRING |  |  |  |  |  |
| `record_id` | Record Id | STRING | record_id |  |  |  |  |
| `activity_type` | 活动类型 | STRING | 浏览未购、老客复购 view_new, olduser_buy |  |  |  |  |
| `product_sku` | 商品SKU | STRING | 只有浏览未购有值，老客复购没值， |  |  |  |  |
| `product_id` | 商品ID | STRING | 只有浏览未购有值，老客复购没值， |  |  |  |  |
| `product_spu` | 商品SPU | STRING | 只有浏览未购有值，老客复购没值， |  |  |  |  |
| `coupon_code` | 优惠券code | STRING | 只有浏览未购有值，老客复购没值， |  |  |  |  |
| `variant_id` | sku id | STRING | 只有浏览未购有值，老客复购没值， |  |  |  |  |
