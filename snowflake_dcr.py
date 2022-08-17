import streamlit as st
import os
import re
import glob


# Runs a series of SQL scripts with some automated replacements
def run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words):
    # Clean up old files
    files = glob.glob(os.getcwd() + "/output/*")
    for f in files:
        os.remove(f)

    # Prepare scripts
    comment_code_regex = re.compile(r"(?<!:)//.*")

    for current_script in script_list:
        print("Starting " + current_script)
        original_script = path + current_script + ".sql"
        prepared_script = "output/" + current_script + "-prepared.sql"
        script_index = script_list.index(current_script)
        script_conn = script_conn_list[script_index]

        with open(original_script, "r", encoding='utf-8') as fin:
            with open(prepared_script, "w", encoding='utf-8') as fout:
                for line in fin:
                    # Prepare temp file
                    for check, replace in zip(check_words, replace_words):
                        line = line.replace(check, replace)

                    # Remove commented SQL lines due to finicky execute_stream behavior
                    line = re.sub(comment_code_regex, '', line)

                    fout.write(line)

        if not is_debug_mode:
            print("Running statements for " + current_script)
            with open(prepared_script, "r", encoding='utf-8') as fout:
                # Run script
                for cur in script_conn.execute_stream(fout, remove_comments=True):
                    print(cur.query)
                    for ret in cur:
                        print(ret)
        else:
            print("Debug mode: File generated but not run for" + current_script)


# Deploys 2-party DCRs
def deploy(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account, consumer_conn,
           abbreviation):
    if dcr_version == "6.0 Native App":
        if abbreviation == "":
            abbreviation = "demo"

        if st.secrets["local_dcr_v6_path"] == "":
            path = os.getcwd() + "/data-clean-room-tng/"
        else:
            path = st.secrets["local_dcr_v6_path"]

        script_list = ["provider_init", "provider_templates",
                       "consumer_init",
                       "provider_enable_consumer", "provider_ml",
                       "consumer_ml"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn, provider_conn,
                            consumer_conn]

        check_words = ["SNOWCAT2", "snowcat2", "SNOWCAT", "snowcat", "_DEMO_", "_demo_"]
        replace_words = [provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 Jinja":
        if abbreviation == "":
            abbreviation = "samp"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_init", "provider_templates_jinja",
                       "consumer_init",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["select dcr_samp_app.cleanroom.get_sql_js(", "select dcr_samp_provider_db.cleanroom.get_sql_js(",
                       "dcr_samp_provider_db.cleanroom.get_sql_js(template, request_params) as valid_sql",
                       "PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = ["select dcr_samp_consumer.util.get_sql_jinja(",
                         "select dcr_samp_provider_db.templates.get_sql_jinja(",
                         "dcr_samp_provider_db.templates.get_sql_jinja(template, request_params) as valid_sql",
                         provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_", ""]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 SQL Param":
        if abbreviation == "":
            abbreviation = "samp"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_init", "provider_templates_js",
                       "consumer_init",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = [provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "ID Resolution Native App":
        # TODO - Automate ID Resolution
        var = None


# Adds consumers to existing Provider DCRs
def add_consumer(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account,
                 consumer_conn, abbreviation):
    if dcr_version == "6.0 Native App":
        if abbreviation == "":
            abbreviation = "demo"

        if st.secrets["local_dcr_v6_path"] == "":
            path = os.getcwd() + "/data-clean-room-tng/"
        else:
            path = st.secrets["local_dcr_v6_path"]

        script_list = ["provider_init_new_consumer",
                       "consumer_init",
                       "provider_enable_consumer", "provider_ml",
                       "consumer_ml"]
        script_conn_list = [provider_conn,
                            consumer_conn,
                            provider_conn, provider_conn,
                            consumer_conn]

        check_words = ["SNOWCAT4", "snowcat4", "SNOWCAT2", "snowcat2", "SNOWCAT", "snowcat", "_DEMO_", "_demo_"]
        replace_words = [consumer_account, consumer_account, provider_account, provider_account, consumer_account,
                         consumer_account, "_" + abbreviation + "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 Jinja":
        if abbreviation == "":
            abbreviation = "samp"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_templates_jinja", "provider_add_consumer_to_share",
                       "consumer_init",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["select dcr_samp_app.cleanroom.get_sql_js(", "select dcr_samp_provider_db.cleanroom.get_sql_js(",
                       "dcr_samp_provider_db.cleanroom.get_sql_js(template, request_params) as valid_sql",
                       "PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = ["select dcr_samp_consumer.util.get_sql_jinja(",
                         "select dcr_samp_provider_db.templates.get_sql_jinja(",
                         "dcr_samp_provider_db.templates.get_sql_jinja(template, request_params) as valid_sql",
                         provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_", ""]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 SQL Param":
        if abbreviation == "":
            abbreviation = "samp"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_templates_js", "provider_add_consumer_to_share",
                       "consumer_init",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = [provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)


# Adds providers to existing DCRs
def add_provider(is_debug_mode, dcr_version, provider_account, provider_conn, consumer_account, consumer_conn,
                 abbreviation, app_suffix):
    if dcr_version == "6.0 Native App":
        if abbreviation == "":
            abbreviation = "demo"
        if app_suffix == "":
            app_suffix = "two"

        if st.secrets["local_dcr_v6_path"] == "":
            path = os.getcwd() + "/data-clean-room-tng/"
        else:
            path = st.secrets["local_dcr_v6_path"]

        script_list = ["provider_init", "provider_templates",
                       "consumer_init_new_provider",
                       "provider_enable_consumer", "provider_ml",
                       "consumer_ml"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn, provider_conn,
                            consumer_conn]

        check_words = ["dcr_demo_app_two", "DCR_DEMO_APP_TWO", "SNOWCAT3", "snowcat3", "SNOWCAT2", "snowcat2",
                       "SNOWCAT", "snowcat", "_DEMO_", "_demo_"]
        replace_words = ["dcr_demo_app_" + app_suffix, "dcr_demo_app_" + app_suffix, provider_account, provider_account,
                         provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 Jinja":
        if abbreviation == "":
            abbreviation = "samp"
        if app_suffix == "":
            app_suffix = "two"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_init", "provider_templates_jinja",
                       "consumer_init_new_provider",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["dcr_samp_app_two", "DCR_SAMP_APP_TWO",
                       "select dcr_samp_app.cleanroom.get_sql_js(", "select dcr_samp_provider_db.cleanroom.get_sql_js(",
                       "dcr_samp_provider_db.cleanroom.get_sql_js(template, request_params) as valid_sql",
                       "PROVIDER2_ACCT", "provider2_acct", "PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT",
                       "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = ["dcr_samp_app_" + app_suffix, "dcr_samp_app_" + app_suffix,
                         "select dcr_samp_consumer.util.get_sql_jinja(",
                         "select dcr_samp_provider_db.templates.get_sql_jinja(",
                         "dcr_samp_provider_db.templates.get_sql_jinja(template, request_params) as valid_sql",
                         provider_account, provider_account, provider_account, provider_account, consumer_account,
                         consumer_account, "_" + abbreviation + "_", "_" + abbreviation + "_", ""]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 SQL Param":
        if abbreviation == "":
            abbreviation = "samp"
        if app_suffix == "":
            app_suffix = "two"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        script_list = ["provider_init", "provider_templates_js",
                       "consumer_init_new_provider",
                       "provider_enable_consumer"]
        script_conn_list = [provider_conn, provider_conn,
                            consumer_conn,
                            provider_conn]

        check_words = ["dcr_samp_app_two", "DCR_SAMP_APP_TWO", "PROVIDER2_ACCT", "provider2_acct",
                       "PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = ["dcr_samp_app_" + app_suffix, "dcr_samp_app_" + app_suffix, provider_account, provider_account,
                         provider_account, provider_account, consumer_account, consumer_account, "_" + abbreviation +
                         "_", "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)


# Upgrades DCRs from v5.5 to v6.0
def upgrade(is_debug_mode, provider_account, provider_conn, consumer_account, consumer_conn, new_abbreviation,
            old_abbreviation):
    if new_abbreviation == "":
        new_abbreviation = "demo"

    if old_abbreviation == "":
        old_abbreviation = "samp"

    if st.secrets["local_dcr_v6_path"] == "":
        path = os.getcwd() + "/data-clean-room-tng/"
    else:
        path = st.secrets["local_dcr_v6_path"]

    script_list = ["provider_init", "provider_upgrade",
                   "consumer_init",
                   "provider_enable_consumer", "provider_ml",
                   "consumer_ml"]
    script_conn_list = [provider_conn, provider_conn,
                        consumer_conn,
                        provider_conn, provider_conn,
                        consumer_conn]

    check_words = ["SNOWCAT2", "snowcat2", "SNOWCAT", "snowcat", "_DEMO_", "_demo_", "_SAMP_", "_samp_"]
    replace_words = [provider_account, provider_account, consumer_account, consumer_account,
                     "_" + new_abbreviation + "_",
                     "_" + new_abbreviation + "_", "_" + old_abbreviation + "_", "_" + old_abbreviation + "_"]

    run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)


# Uninstalls DCRs for an account (provider or consumer)
def uninstall(is_debug_mode, dcr_version, account_type, account, account_conn, consumer_account, abbreviation,
              app_suffix):
    if dcr_version == "6.0 Native App":
        if abbreviation == "":
            abbreviation = "demo"

        if st.secrets["local_dcr_v6_path"] == "":
            path = os.getcwd() + "/data-clean-room-tng/"
        else:
            path = st.secrets["local_dcr_v6_path"]

        check_words = ["SNOWCAT2", "snowcat2", "SNOWCAT", "snowcat", "_DEMO_", "_demo_"]
        replace_words = [account, account, consumer_account, consumer_account, "_" + abbreviation + "_",
                         "_" + abbreviation + "_"]

        if account_type == "Provider":
            script_list = ["provider_uninstall"]
            script_conn_list = [account_conn]
        elif account_type == "Consumer":
            script_list = ["consumer_uninstall"]
            script_conn_list = [account_conn]
            # Support for multi-provider
            if app_suffix != "":
                check_words.append("_app")
                replace_words.append("_app_" + app_suffix)
                check_words.append("_APP")
                replace_words.append("_app_" + app_suffix)
        else:
            script_list = []
            script_conn_list = []

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)
    elif dcr_version == "5.5 Jinja" or dcr_version == "5.5 SQL Param":
        if abbreviation == "":
            abbreviation = "samp"

        if st.secrets["local_dcr_v55_path"] == "":
            path = os.getcwd() + "/data-clean-room/"
        else:
            path = st.secrets["local_dcr_v55_path"]

        if account_type == "Provider":
            script_list = ["provider_uninstall"]
            script_conn_list = [account_conn]
        elif account_type == "Consumer":
            script_list = ["consumer_uninstall"]
            script_conn_list = [account_conn]
        else:
            script_list = []
            script_conn_list = []

        check_words = ["PROVIDER_ACCT", "provider_acct", "CONSUMER_ACCT", "consumer_acct", "_SAMP_", "_samp_"]
        replace_words = [account, account, consumer_account, consumer_account, "_" + abbreviation + "_",
                         "_" + abbreviation + "_"]

        run_scripts(is_debug_mode, path, script_list, script_conn_list, check_words, replace_words)

