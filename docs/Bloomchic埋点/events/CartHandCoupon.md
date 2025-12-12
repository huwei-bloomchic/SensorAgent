# CartHandCoupon

## 基本信息

- **事件显示名**: 手动用券结果（手动用券，点击【apply】）
- **事件英文名**: `CartHandCoupon`
- **所属模块**: 4.【购物车】埋点
- **应埋点平台**: Android,iOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `coupon_code` | 券的code | STRING | 手动输入的券code | APP3.6新增 |  | 购物车-Add Promo Code模块 |  |
| `is_apply_successfully` | 是否应用成功 | int | 否/是,用0和1来表示，1表成功，0表失败 |  |  |  |  |
