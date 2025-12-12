# SwitchSitePageClick

## 基本信息

- **事件显示名**: 站点切换弹窗点击
- **事件英文名**: `SwitchSitePageClick`
- **所属模块**: 0.APP特有的埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `target_country` | 目标国家 | STRING |  |  |  |  |  |
| `target_site_code` | 目标站点 | STRING |  |  |  |  |  |
| `url` | deeplink URL | STRING |  |  |  |  |  |
| `type` | 弹窗类型：deeplink,auto,manual | STRING | 3.15版本 站点切换 3.28 登录流程优化，加入登录切站点 |  |  |  |  |
| `click_type` | 点击类型：switch, stay,close | STRING |  |  |  |  |  |
