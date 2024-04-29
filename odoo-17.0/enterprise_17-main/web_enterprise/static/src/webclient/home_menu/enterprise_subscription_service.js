/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";
import { deserializeDateTime, serializeDate, formatDate } from "@web/core/l10n/dates";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ExpirationPanel } from "./expiration_panel";
import { cookie } from "@web/core/browser/cookie";

const { DateTime } = luxon;
import { Component, xml, useState } from "@odoo/owl";


export class SubscriptionManager {

}

class ExpiredSubscriptionBlockUI extends Component {
    setup() {
        this.subscription = useState(useService("enterprise_subscription"));
    }
}
ExpiredSubscriptionBlockUI.props = {};
ExpiredSubscriptionBlockUI.template = xml`
//<t t-if="subscription.daysLeft &lt;= 0">
//    <div class="o_blockUI"/>
//    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: 1100" class="d-flex align-items-center justify-content-center">
//        <ExpirationPanel/>
//    </div>
//</t>`;
ExpiredSubscriptionBlockUI.components = { ExpirationPanel };

export const enterpriseSubscriptionService = {
    name: "enterprise_subscription",
    dependencies: ["orm", "rpc", "notification"],
    start(env, { rpc, orm, notification }) {
        registry
            .category("main_components")
            .add("expired_subscription_block_ui", { Component: ExpiredSubscriptionBlockUI });
        return new SubscriptionManager(env, { rpc, orm, notification });
    },
};

registry.category("services").add("enterprise_subscription", enterpriseSubscriptionService);
