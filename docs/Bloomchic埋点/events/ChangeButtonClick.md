# ChangeButtonClick

## 基本信息

- **事件显示名**: 点击Change按钮
- **事件英文名**: `ChangeButtonClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,Web

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_name` | 所在页面名称 | STRING | Shipping、Payment | JavaScript | Shipping或Payment页面<br/>点击Change按钮时上报 | 11.15 星期一 19:40生效 |  |
| `change_context` | 更改的内容 | STRING | 用户在Shipping、Payment页面更改的内容<br/>1=Contact<br/>2=ShippingAddress<br/>3=ShippingMethod | JavaScript |  |  |  |
