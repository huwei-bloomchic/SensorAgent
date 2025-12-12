# ActivityManualReceive

## 基本信息

- **事件显示名**: 手动领取活动
- **事件英文名**: `ActivityManualReceive`
- **所属模块**: 9.【活动】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 首页、商品列表、商品详情页、thankyou页、me页、其他 |  |  |  |  |
| `popup_from` | 弹窗来源 | STRING | 活动触发、用户点击 【 loop_tigger, click_tigger 】 |  |  |  |  |
| `activity_id` | 活动id | STRING |  |  |  |  |  |
| `activity_name` | 活动名 | STRING |  |  |  |  |  |
| `scene_id` | 场景id | STRING | 后端的record_id |  |  |  |  |
| `record_id` | Record Id | STRING | record_id |  |  |  |  |
| `coupon_code` | 优惠券code | STRING |  |  |  |  |  |
| `skip_page_url` | 跳转页面url | STRING | 点击后的跳链 |  |  |  |  |
| `is_succeed_coupon` | 获取券成功 | STRING | true / false |  |  |  |  |
| `failed_reason` | 失败原因 |  |  |  |  |  |  |
