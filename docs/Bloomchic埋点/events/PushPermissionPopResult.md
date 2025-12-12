# PushPermissionPopResult

## 基本信息

- **事件显示名**: AppPush前置引导通知权限结果
- **事件英文名**: `PushPermissionPopResult`
- **所属模块**: 5.【checkout到下单支付】埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `page_code` | 页面位置 | STRING | 支付完成页、Track页面、启屏页、我的、 订单列表页、商详缺货提醒弹窗 |  |  |  |  |
| `permission` | 权限结果 | Int | 1: 有通知权限 0：无通知权限 |  |  |  |  |
