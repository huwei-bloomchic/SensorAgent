# CheckoutRewardsRedeem

## 基本信息

- **事件显示名**: 结算-券&giftcard兑换
- **事件英文名**: `CheckoutRewardsRedeem`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `type` |  | STRING | coupon 优惠券 giftcard 礼品卡 |  |  |  |  |
| `id` |  | STRING | 兑换id |  | 去除，这个字段上报不了，换成 reward_id |  |  |
| `error_msg: 兑换失败信息` |  | STRING | 成功无，失败有 |  |  |  |  |
| `reward_id` |  | STRING | 兑换id |  |  |  |  |
