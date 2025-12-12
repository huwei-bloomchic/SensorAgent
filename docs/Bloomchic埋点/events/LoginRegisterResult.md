# LoginRegisterResult

## 基本信息

- **事件显示名**: 登录注册成功
- **事件英文名**: `LoginRegisterResult`
- **所属模块**: 0.全局埋点
- **应埋点平台**: 服务端

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `email` | 登录邮箱 | STRING |  |  | 之前是前端报，现在换成服务端报，<br/>把RegisterResult和LoginResult两个事件合并成1个 |  |  |
| `is_new_user` | 是否新注册 | BOOL | true=新注册，<br/>false=老用户登录 |  |  |  |  |
