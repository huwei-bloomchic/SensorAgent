# MemberNotifDialogShow

## 基本信息

- **事件显示名**: 会员通知弹窗展示
- **事件英文名**: `MemberNotifDialogShow`
- **所属模块**: 8.【会员】埋点
- **应埋点平台**: Android,Web,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `type` | type为1表示生日弹窗，为2表示升降级弹窗，直接用后端返回的值即可 | INT |  |  |  |  |  |
| `email` | 用户邮箱 | STRING |  |  |  |  |  |
| `title` | 弹窗的标题，后端返回的title字段 | STRING |  |  |  |  |  |
| `notice_id` | 后端返回当前通知弹窗的唯一id | INT |  |  |  |  |  |
| `link` | 跳转的链接 | STRING |  |  |  |  |  |
| `level_name` | 用户等级名 | STRING |  |  |  |  |  |
