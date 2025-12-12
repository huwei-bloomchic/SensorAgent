# PushPermissionPopClick

## 基本信息

- **事件显示名**: AppPush前置引导弹窗点击
- **事件英文名**: `PushPermissionPopClick`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 支付完成页、Track页面、启屏页、我的、 订单列表页、商详缺货提醒弹窗 |  |  |  |  |
| `click_type` | 点击弹窗类型 | STRING | OK、关闭 |  | 点击启屏页的skip按钮上报关闭，点击启屏页的enable now按钮上报OK |  |  |
