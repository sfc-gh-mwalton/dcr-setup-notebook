import streamlit as st
import snowflake_conn as sfc
import snowflake_dcr as dcr

# Page settings
st.set_page_config(
    page_title="DCR Setup Assistant",
    page_icon="❄️️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/snowflakecorp/dcr-setup-assistant',
        'Report a bug': "https://github.com/snowflakecorp/dcr-setup-assistant",
        'About': "This app helps deploy and manage DCRs!"
    }
)

# Set up main page
col1, col2 = st.columns((6, 1))
col1.title("🐻‍❄ DCR SETUP ASSISTANT 🐻‍❄️")
col2.image("assets/snowflake_dcr_multi.png", width=120)
st.sidebar.image("assets/bear_snowflake_hello.png")
action = st.sidebar.radio("What action would you like to take?", ("Initial Deployment 🐻‍❄", "Add Add'l Consumer 🐧️",
                                                                  "Add Add'l Provider ☃️", "Upgrade 🧊",
                                                                  "Uninstall 💧"))

# Get list of accounts
accounts = []
account_nicknames = []
accounts_count = 1
while "account_" + str(accounts_count) in st.secrets:
    account = st.secrets["account_" + str(accounts_count)]["account"].upper()
    nickname = st.secrets["account_" + str(accounts_count)]["nickname"].upper() + " - " + account
    if account != "":
        accounts.append(account)
        account_nicknames.append(nickname)
    accounts_count += 1

# Store accounts in session state
st.session_state['accounts'] = accounts
st.session_state['account_nicknames'] = account_nicknames

# Build form based on selected action
if action == "Initial Deployment 🐻‍❄":
    # Form for initial deployment
    st.subheader("❄️ Initial DCR Deployment! ❄️")
    with st.form("initial_deployment_form"):
        dcr_version = st.selectbox("Which version do you want to install?",
                                   ["6.0 Native App", "5.5 Jinja", "5.5 SQL Param"])  # , "ID Resolution Native App"])
        abbreviation = st.text_input("What database abbreviation would you like? (Leave blank for default)")
        provider_nickname = st.selectbox("Which Provider account?", st.session_state['account_nicknames'])
        consumer_nickname = st.selectbox("Which Consumer account?", st.session_state['account_nicknames'])
        # Debug mode prevents actually running the script, but outputs the script contents
        is_debug_mode = st.checkbox("Run in debug mode (generate scripts, but not run them)", True)

        # Get accounts from session_state
        provider_index = st.session_state['account_nicknames'].index(provider_nickname)
        provider_account = st.session_state['accounts'][provider_index]
        consumer_index = st.session_state['account_nicknames'].index(consumer_nickname)
        consumer_account = st.session_state['accounts'][consumer_index]

        submitted = st.form_submit_button("Deploy")

        if submitted:
            if provider_account == consumer_account:
                st.error("Provider and consumer cannot be the same account!")
            else:
                # Establish connections, if necessary
                if is_debug_mode:
                    provider_conn = None
                    consumer_conn = None
                else:
                    provider_conn = sfc.init_connection("account_" + str(provider_index + 1))
                    consumer_conn = sfc.init_connection("account_" + str(consumer_index + 1))

                with st.spinner("Deploying Clean Room..."):
                    dcr.deploy(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account,
                               consumer_conn, abbreviation)

                # Message dependent on debug or not
                if is_debug_mode:
                    st.success("Scripts Generated in Output!")
                else:
                    st.success("Clean Room Deployed!")
                st.snow()

elif action == "Add Add'l Consumer 🐧️":
    # Form for adding consumers
    st.subheader("❄️ Add Consumers to Existing DCRs! ❄️")
    with st.form("additional_consumer_form"):
        dcr_version = st.selectbox("Which version does the Provider have installed?",
                                   ["6.0 Native App", "5.5 Jinja", "5.5 SQL Param"])
        abbreviation = st.text_input("What database abbreviation does the Provider have? (Leave blank for default)")
        provider_nickname = st.selectbox("Which is the existing Provider account?",
                                         st.session_state['account_nicknames'])
        consumer_nickname = st.selectbox("Which is the new Consumer account?", st.session_state['account_nicknames'])
        # Debug mode prevents actually running the script, but outputs the script contents
        is_debug_mode = st.checkbox("Run in debug mode (generate scripts, but not run them)", True)

        # Get accounts from session_state
        provider_index = st.session_state['account_nicknames'].index(provider_nickname)
        provider_account = st.session_state['accounts'][provider_index]
        consumer_index = st.session_state['account_nicknames'].index(consumer_nickname)
        consumer_account = st.session_state['accounts'][consumer_index]

        submitted = st.form_submit_button("Add Consumer")

        if submitted:
            if provider_account == consumer_account:
                st.error("Provider and consumer cannot be the same account!")
            else:
                # Establish connections, if necessary
                if is_debug_mode:
                    provider_conn = None
                    consumer_conn = None
                else:
                    provider_conn = sfc.init_connection("account_" + str(provider_index + 1))
                    consumer_conn = sfc.init_connection("account_" + str(consumer_index + 1))

                with st.spinner("Adding Consumer..."):
                    dcr.add_consumer(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account,
                                     consumer_conn, abbreviation)

                # Message dependent on debug or not
                if is_debug_mode:
                    st.success("Scripts Generated in Output!")
                else:
                    st.success("Consumer Added!")
                st.snow()

elif action == "Add Add'l Provider ☃️":
    # Form for adding providers
    st.subheader("❄️ Add Providers to Existing DCRs! ❄️")
    with st.form("additional_provider_form"):
        dcr_version = st.selectbox("Which version does the Consumer have installed?",
                                   ["6.0 Native App", "5.5 Jinja", "5.5 SQL Param"])
        abbreviation = st.text_input("What database abbreviation does the Consumer use? (Leave blank for default)")
        consumer_nickname = st.selectbox("Which is the existing Consumer account?",
                                         st.session_state['account_nicknames'])
        provider_nickname = st.selectbox("Which is the new Provider account?", st.session_state['account_nicknames'])
        app_suffix = st.text_input("What suffix would you like for the Consumer-side app name? (Leave blank for "
                                   "default)")
        # Debug mode prevents actually running the script, but outputs the script contents
        is_debug_mode = st.checkbox("Run in debug mode (generate scripts, but not run them)", True)

        # Get accounts from session_state
        provider_index = st.session_state['account_nicknames'].index(provider_nickname)
        provider_account = st.session_state['accounts'][provider_index]
        consumer_index = st.session_state['account_nicknames'].index(consumer_nickname)
        consumer_account = st.session_state['accounts'][consumer_index]

        submitted = st.form_submit_button("Add Provider")

        if submitted:
            if provider_account == consumer_account:
                st.error("Provider and consumer cannot be the same account!")
            else:
                # Establish connections, if necessary
                if is_debug_mode:
                    provider_conn = None
                    consumer_conn = None
                else:
                    provider_conn = sfc.init_connection("account_" + str(provider_index + 1))
                    consumer_conn = sfc.init_connection("account_" + str(consumer_index + 1))

                with st.spinner("Adding Provider..."):
                    dcr.add_provider(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account,
                                     consumer_conn, abbreviation, app_suffix)

                # Message dependent on debug or not
                if is_debug_mode:
                    st.success("Scripts Generated in Output!")
                else:
                    st.success("Provider Added!")
                st.snow()

elif action == "Upgrade 🧊":
    # Form for upgrading
    st.subheader("❄️ Upgrade Existing v5.5 DCRs to v6.0! ❄️")
    with st.form("upgrade_form"):
        new_abbreviation = st.text_input("What database abbreviation would you like for the **new** v6.0 DCR? (Leave "
                                         "blank for default)")
        old_abbreviation = st.text_input("What is the database abbreviation of the **old** v5.5 DCR? (Leave blank for "
                                         "default)")
        provider_nickname = st.selectbox("Which Provider account are you upgrading?",
                                         st.session_state['account_nicknames'])
        consumer_nickname = st.selectbox("Which Consumer account?",
                                         st.session_state['account_nicknames'])
        # Debug mode prevents actually running the script, but outputs the script contents
        is_debug_mode = st.checkbox("Run in debug mode (generate scripts, but not run them)", True)

        # Get accounts from session_state
        provider_index = st.session_state['account_nicknames'].index(provider_nickname)
        provider_account = st.session_state['accounts'][provider_index]
        consumer_index = st.session_state['account_nicknames'].index(consumer_nickname)
        consumer_account = st.session_state['accounts'][consumer_index]

        submitted = st.form_submit_button("Upgrade")

        if submitted:
            if provider_account == consumer_account:
                st.error("Provider and Consumer cannot be the same account!")
            elif new_abbreviation == old_abbreviation and (new_abbreviation != "" or old_abbreviation != ""):
                st.error("Old and new database abbreviation cannot match!")
            else:
                # Establish connections, if necessary
                if is_debug_mode:
                    provider_conn = None
                    consumer_conn = None
                else:
                    provider_conn = sfc.init_connection("account_" + str(provider_index + 1))
                    consumer_conn = sfc.init_connection("account_" + str(consumer_index + 1))

                with st.spinner("Updating Clean Room..."):
                    dcr.upgrade(is_debug_mode, provider_account, provider_conn, consumer_account, consumer_conn,
                                new_abbreviation, old_abbreviation)

                # Message dependent on debug or not
                if is_debug_mode:
                    st.success("Scripts Generated in Output!")
                else:
                    st.success("Clean Room Upgraded!")
                st.snow()

elif action == "Uninstall 💧":
    # Form for uninstalling
    st.subheader("❄️ Uninstall Existing DCRs! ❄️")
    st.warning("This action **drops** related shares and databases!")
    with st.form("initial_deployment_form"):
        dcr_version = st.selectbox("Which version do you want to uninstall?",
                                   ["6.0 Native App", "5.5 Jinja", "5.5 SQL Param"])  # , "ID Resolution Native App"])
        abbreviation = st.text_input(
            "What database abbreviation would you like to uninstall? (Leave blank for default)")
        account_nickname = st.selectbox("Which account to uninstall?", st.session_state['account_nicknames'])
        account_type = st.selectbox("What is the account type for the account being uninstalled?", ["Consumer",
                                                                                                    "Provider"])

        consumer_accounts_options = st.session_state['account_nicknames']
        consumer_accounts_options.insert(0, "")
        consumer_nickname = st.selectbox("Which Consumer account (if uninstalling Provider)?",
                                         consumer_accounts_options)
        app_suffix = st.text_input("What suffix would you like for the Consumer-side app name? (Leave blank for "
                                   "default)")
        # Debug mode prevents actually running the script, but outputs the script contents
        is_debug_mode = st.checkbox("Run in debug mode (generate scripts, but not run them)", True)

        # Get accounts from session_state
        account_index = st.session_state['account_nicknames'].index(account_nickname)
        account = st.session_state['accounts'][account_index]
        if consumer_nickname != "":
            consumer_index = st.session_state['account_nicknames'].index(consumer_nickname) - 1
            consumer_account = st.session_state['accounts'][consumer_index]
        else:
            consumer_account = ""

        st.warning("Submitting while not in debug mode will **drop** related shares and databases")
        submitted = st.form_submit_button("Uninstall")

        if submitted:
            if account == consumer_account and account_type == "Provider":
                st.error("Provider and Consumer cannot be the same account!")
            else:
                # Establish connections, if necessary
                if is_debug_mode:
                    account_conn = None
                else:
                    account_conn = sfc.init_connection("account_" + str(account_index + 1))

                with st.spinner("Uninstalling Clean Room..."):
                    dcr.uninstall(is_debug_mode, dcr_version, account_type, account, account_conn, consumer_account,
                                  abbreviation, app_suffix)

                # Message dependent on debug or not
                if is_debug_mode:
                    st.success("Scripts Generated in Output!")
                else:
                    st.success("Clean Room Uninstalled!")
                st.snow()
