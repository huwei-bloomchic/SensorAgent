# af_first_launch

## 基本信息

- **事件显示名**: AppsFlyer 回调onConversionDataSuccess，<br/>is_first_launch = true 时候上报<br/>AF归因成功首次启动<br/>Android 2.10/iOS 2.8版本新增
- **事件英文名**: `af_first_launch`
- **所属模块**: 0.APP特有的埋点
- **应埋点平台**: Android,IOS

## 事件属性

| 属性英文名 | 属性显示名 | 数据类型 | 属性值示例或说明 | 应埋点平台 | 触发时机 | 备注 | 日期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `af_conversion_data` | AF会话归因整个JSON数据， 为了避免JSON数据过长导致神策截取自断，因此排除 af_android_url,af_web_dp,af_ios_url,af_dp,deep_link_value | String | onConversionDataSuccess回调的整个JSON数据 |  |  |  |  |
| `utm_medium` | utm_medium | String | onConversionDataSuccess回调数据utm_medium |  |  |  |  |
| `bc_id` | bc_id | String | onConversionDataSuccess回调数据bc_id |  |  |  |  |
| `af_channel` | af_channel | String | onConversionDataSuccess回调数据af_channel |  |  |  |  |
| `utm_content` | utm_content | String | onConversionDataSuccess回调数据utm_content |  |  |  |  |
| `install_time` | install_time | String | onConversionDataSuccess回调数据install_time |  |  |  |  |
| `af_dp` | af_dp | String | onConversionDataSuccess回调数据af_dp |  |  |  |  |
| `deep_link_value` | deep_link_value | String | onConversionDataSuccess回调数据deep_link_value |  |  |  |  |
| `media_source` | media_source | String | onConversionDataSuccess回调数据media_source |  |  |  |  |
| `utm_campaign` | utm_campaign | String | onConversionDataSuccess回调数据utm_campaign |  |  |  |  |
| `af_status` | af_status | String | onConversionDataSuccess回调数据af_status |  |  |  |  |
| `utm_term` | utm_term | String | onConversionDataSuccess回调数据utm_term |  |  |  |  |
| `campaign` | campaign | String | onConversionDataSuccess回调数据campaign |  |  |  |  |
| `http_referrer` | http_referrer | String | onConversionDataSuccess回调数据 http_referrer |  |  |  |  |
