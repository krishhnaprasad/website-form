/** @odoo-module **/

import { hasTouch, isIosApp, isMacOS } from "@web/core/browser/feature_detection";
import { useHotkey } from "@web/core/hotkeys/hotkey_hook";
import { useService } from "@web/core/utils/hooks";
import { ExpirationPanel } from "./expiration_panel";
import { useSortable } from "@web/core/utils/sortable_owl";
import { reorderApps } from "@web/webclient/menus/menu_helpers";

import {
    Component,
    useExternalListener,
    onMounted,
    onPatched,
    onWillUpdateProps,
    useState,
    useRef,
} from "@odoo/owl";

class FooterComponent extends Component {
    setup() {
        this.controlKey = isMacOS() ? "COMMAND" : "CONTROL";
    }
}
FooterComponent.template = "web_enterprise.HomeMenu.CommandPalette.Footer";
FooterComponent.props = {
    switchNamespace: { type: Function, optional: true },
};

export class HomeMenu extends Component {

    setup() {
        this.command = useService("command");
        this.menus = useService("menu");
        this.user = useService("user");
        this.homeMenuService = useService("home_menu");
        this.subscription = useState(useService("enterprise_subscription"));
        this.ui = useService("ui");
        this.state = useState({
            focusedIndex: null,
            isIosApp: isIosApp(),
        });
        this.inputRef = useRef("input");
        this.rootRef = useRef("root");
        this.pressTimer;
        this.apps = useState(this.props.apps);

        if (!this.env.isSmall) {
            this._registerHotkeys();
        }

        useSortable({
            enable: this._enableAppsSorting,
            ref: this.rootRef,
            elements: ".o_draggable",
            cursor: "move",
            delay: 500,
            tolerance: 10,
            onWillStartDrag: (params) => this._sortStart(params),
            onDrop: (params) => this._sortAppDrop(params),
        });

        onWillUpdateProps(() => {
            this.state.focusedIndex = null;
        });

        onMounted(() => {
            if (!hasTouch()) {
                this._focusInput();
            }
        });

        onPatched(() => {
            if (this.state.focusedIndex !== null && !this.env.isSmall) {
                const selectedItem = document.querySelector(".o_home_menu .o_menuitem.o_focused");
                // When TAB is managed externally the class o_focused disappears.
                if (selectedItem) {
                    // Center window on the focused item
                    selectedItem.scrollIntoView({ block: "center" });
                }
            }
        });
    }


    get displayedApps() {
        return this.apps;
    }


    get maxIconNumber() {
        const w = window.innerWidth;
        if (w < 576) {
            return 3;
        } else if (w < 768) {
            return 4;
        } else {
            return 6;
        }
    }


    _openMenu(menu) {
        return this.menus.selectMenu(menu);
    }


    _updateFocusedIndex(cmd) {
        const nbrApps = this.displayedApps.length;
        const lastIndex = nbrApps - 1;
        const focusedIndex = this.state.focusedIndex;
        if (lastIndex < 0) {
            return;
        }
        if (focusedIndex === null) {
            this.state.focusedIndex = 0;
            return;
        }
        const lineNumber = Math.ceil(nbrApps / this.maxIconNumber);
        const currentLine = Math.ceil((focusedIndex + 1) / this.maxIconNumber);
        let newIndex;
        switch (cmd) {
            case "previousElem":
                newIndex = focusedIndex - 1;
                break;
            case "nextElem":
                newIndex = focusedIndex + 1;
                break;
            case "previousColumn":
                if (focusedIndex % this.maxIconNumber) {
                    newIndex = focusedIndex - 1;
                } else {
                    newIndex =
                        focusedIndex + Math.min(lastIndex - focusedIndex, this.maxIconNumber - 1);
                }
                break;
            case "nextColumn":
                if (focusedIndex === lastIndex || (focusedIndex + 1) % this.maxIconNumber === 0) {
                    newIndex = (currentLine - 1) * this.maxIconNumber;
                } else {
                    newIndex = focusedIndex + 1;
                }
                break;
            case "previousLine":
                if (currentLine === 1) {
                    newIndex = focusedIndex + (lineNumber - 1) * this.maxIconNumber;
                    if (newIndex > lastIndex) {
                        newIndex = lastIndex;
                    }
                } else {
                    newIndex = focusedIndex - this.maxIconNumber;
                }
                break;
            case "nextLine":
                if (currentLine === lineNumber) {
                    newIndex = focusedIndex % this.maxIconNumber;
                } else {
                    newIndex =
                        focusedIndex + Math.min(this.maxIconNumber, lastIndex - focusedIndex);
                }
                break;
        }
        if (newIndex < 0) {
            newIndex = lastIndex;
        } else if (newIndex > lastIndex) {
            newIndex = 0;
        }
        this.state.focusedIndex = newIndex;
    }

    _focusInput() {
        if (!this.env.isSmall && this.inputRef.el) {
            this.inputRef.el.focus({ preventScroll: true });
        }
    }

    _enableAppsSorting() {
        return true;
    }


    _sortAppDrop({ element, previous }) {
        const order = this.props.apps.map((app) => app.xmlid);
        const elementId = element.children[0].dataset.menuXmlid;
        const elementIndex = order.indexOf(elementId);
        order.splice(elementIndex, 1);
        if (previous) {
            const prevIndex = order.indexOf(previous.children[0].dataset.menuXmlid);
            order.splice(prevIndex + 1, 0, elementId);
        } else {
            order.splice(0, 0, elementId);
        }
        reorderApps(this.apps, order);
        this.user.setUserSettings("homemenu_config", JSON.stringify(order));
    }


    _sortStart({ element, addClass }) {
        addClass(element.children[0], "o_dragged_app");
    }


    _onAppClick(app) {
        this._openMenu(app);
    }

    _registerHotkeys() {
        const hotkeys = [
            ["ArrowDown", () => this._updateFocusedIndex("nextLine")],
            ["ArrowRight", () => this._updateFocusedIndex("nextColumn")],
            ["ArrowUp", () => this._updateFocusedIndex("previousLine")],
            ["ArrowLeft", () => this._updateFocusedIndex("previousColumn")],
            ["Tab", () => this._updateFocusedIndex("nextElem")],
            ["shift+Tab", () => this._updateFocusedIndex("previousElem")],
            [
                "Enter",
                () => {
                    const menu = this.displayedApps[this.state.focusedIndex];
                    if (menu) {
                        this._openMenu(menu);
                    }
                },
            ],
            ["Escape", () => this.homeMenuService.toggle(false)],
        ];
        hotkeys.forEach((hotkey) => {
            useHotkey(...hotkey, {
                allowRepeat: true,
            });
        });
        useExternalListener(window, "keydown", this._onKeydownFocusInput);
    }

    _onKeydownFocusInput() {
        if (
            document.activeElement !== this.inputRef.el &&
            this.ui.activeElement === document &&
            !["TEXTAREA", "INPUT"].includes(document.activeElement.tagName)
        ) {
            this._focusInput();
        }
    }

    _onInputSearch() {
        const onClose = () => {
            this._focusInput();
            this.inputRef.el.value = "";
        };
        const searchValue = this.compositionStart ? "/" : `/${this.inputRef.el.value.trim()}`;
        this.compositionStart = false;
        this.command.openMainPalette({ searchValue, FooterComponent }, onClose);
    }

    _onInputBlur() {
        if (hasTouch()) {
            return;
        }

        setTimeout(() => {
            if (document.activeElement === document.body && this.ui.activeElement === document) {
                this._focusInput();
            }
        }, 0);
    }

    _onCompositionStart() {
        this.compositionStart = true;
    }
}
HomeMenu.components = { ExpirationPanel };
HomeMenu.props = {
    apps: {
        type: Array,
        element: {
            type: Object,
            shape: {
                actionID: Number,
                appID: Number,
                id: Number,
                label: String,
                parents: String,
                webIcon: {
                    type: [
                        Boolean,
                        String,
                        {
                            type: Object,
                            optional: 1,
                            shape: {
                                iconClass: String,
                                color: String,
                                backgroundColor: String,
                            },
                        },
                    ],
                    optional: true,
                },
                webIconData: { type: String, optional: 1 },
                xmlid: String,
            },
        },
    },
};
HomeMenu.template = "web_enterprise.HomeMenu";
