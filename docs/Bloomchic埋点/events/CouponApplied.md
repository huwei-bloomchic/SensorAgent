# CouponApplied

## 基本信息

- **事件显示名**: 应用优惠或礼品卡
- **事件英文名**: `CouponApplied`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `coupon_code` | 优惠或礼品卡填写 | STRING | 用户在Information-"gift card or discount code"输入框内填写的内容 | JavaScript | 当用户点击discount code or gift card右侧按钮时上报 |  | Checkout 升级 该事件也可以通过 CheckoutPageClick获取 |
| `position` | 页面位置 | STRING | discount code or gift card右侧按钮 点击时所在的位置 ，比如点击OrderSummary展开项内按钮则报1<br/>1=OrderSummary展开项内的折扣应用按钮点击<br/>2=CheckOut_Payment页面非OrderSummary展开项内的折扣应用按钮点击 | JavaScript |  |  |  |
