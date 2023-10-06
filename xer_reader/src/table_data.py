table_data = {
    "ACCOUNT": {
        "key": "acct_id",
        "description": "Cost Accounts",
        "depends": [],
    },
    "ACTVCODE": {
        "key": "actv_code_id",
        "description": "Activity Code Values",
        "depends": ["ACTVTYPE"],
    },
    "ACTVTYPE": {
        "key": "actv_code_type_id",
        "description": "Activity Codes",
        "depends": [],
    },
    "APPLYACTOPTIONS": {
        "key": None,
        "description": "Apply Actual Options",
        "depends": [],
    },
    "ASGNMNTACAT": {
        "key": None,
        "description": "Assignment Code Assignments",
        "depends": ["ASGNMNTCATTYPE", "ASGNMNTCATVAL", "TASKRSRC"],
    },
    "ASGNMNTCATTYPE": {
        "key": "asgnmnt_catg_type_id",
        "description": "Assignment Codes",
        "depends": [],
    },
    "ASGNMNTCATVAL": {
        "key": "asgnmnt_catg_id",
        "description": "Assignment Code Values",
        "depends": ["ASGNMNTCATTYPE"],
    },
    "BUDGCHNG": {
        "key": "budg_chng_id",
        "description": "Budget Changes",
        "depends": [],
    },
    "CALENDAR": {
        "key": "clndr_id",
        "description": "Calendars",
        "depends": [],
    },
    "COSTTYPE": {
        "key": "cost_type_id",
        "description": "Expense Categories",
        "depends": [],
    },
    "CURRTYPE": {
        "key": "curr_id",
        "description": "Currency Types",
        "depends": [],
    },
    "DOCCATG": {
        "key": "doc_catg_id",
        "description": "Document Categories",
        "depends": [],
    },
    "DOCSTAT": {
        "key": "doc_status_id",
        "description": "Document Statuses",
        "depends": [],
    },
    "DOCUMENT": {
        "key": "doc_id",
        "description": "Work Products and Documents",
        "depends": [],
    },
    "FINDATES": {
        "key": "fin_dates_id",
        "description": "Financial Periods",
        "depends": [],
    },
    "FUNDSRC": {
        "key": "fund_id",
        "description": "Funding Sources",
        "depends": [],
    },
    "ISSUHIST": {
        "key": None,
        "description": "Notification History",
        "depends": [],
    },
    "MEMOTYPE": {
        "key": "memo_type_id",
        "description": "Notebook Topics",
        "depends": [],
    },
    "NONWORK": {
        "key": "nonwork_type_id",
        "description": "Non-work Types",
        "depends": [],
    },
    "OBS": {
        "key": "obs_id",
        "description": "Organization Breakdown Structure",
        "depends": [],
    },
    "PCATTYPE": {
        "key": "proj_catg_type_id",
        "description": "Project Codes",
        "depends": [],
    },
    "PCATVAL": {
        "key": "proj_catg_id",
        "description": "Project Code Values",
        "depends": ["PCATTYPE"],
    },
    "PHASE": {
        "key": "phase_id",
        "description": "Phase Project Code",
        "depends": [],
    },
    "POBS": {
        "key": "pobs_id",
        "description": "Extra Data",
        "depends": [],
    },
    "PROJCOST": {
        "key": "cost_item_id",
        "description": "Project Expenses",
        "depends": ["TASK"],
    },
    "PROJECT": {
        "key": "proj_id",
        "description": "Projects",
        "depends": [],
    },
    "PROJEST": {
        "key": "proj_est_id",
        "description": "Estimate History",
        "depends": [],
    },
    "PROJFUND": {
        "key": "proj_fund_id",
        "description": "Project Funding Assignments",
        "depends": ["FUNDSRC"],
    },
    "PROJISSU": {
        "key": "issue_id",
        "description": "Issues",
        "depends": [],
    },
    "PROJPCAT": {
        "key": None,
        "description": "Project Code Assignments",
        "depends": ["PCATVAL", "PCATTYPE"],
    },
    "PROJTHRS": {
        "key": "thresh_id",
        "description": "Thresholds",
        "depends": [],
    },
    "PROJWBS": {
        "key": "wbs_id",
        "description": "Work Breakdown Structure",
        "depends": [],
    },
    "PRORISK": {
        "key": "risk_id",
        "description": "Risks",
        "depends": ["RISKTYPE"],
    },
    "RCATTYPE": {
        "key": "rsrc_catg_type_id",
        "description": "Resource Codes",
        "depends": [],
    },
    "RCATVAL": {
        "key": "rsrc_catg_id",
        "description": "Resource Code Values",
        "depends": ["RCATTYPE"],
    },
    "RISKTYPE": {
        "key": "risk_type_id",
        "description": "Risk Types",
        "depends": [],
    },
    "ROLECATTYPE": {
        "key": "role_catg_type_id",
        "description": "Role Codes",
        "depends": [],
    },
    "ROLECATVAL": {
        "key": "role_catg_id",
        "description": "Role Code Values",
        "depends": ["ROLECATTYPE"],
    },
    "ROLELIMIT": {
        "key": "rolelimit_id",
        "description": "Role Limits",
        "depends": ["ROLES"],
    },
    "ROLERATE": {
        "key": "role_rate_id",
        "description": "Role Prices",
        "depends": ["ROLES"],
    },
    "ROLERCAT": {
        "key": None,
        "description": "Role Code Assignments",
        "depends": ["ROLES", "ROLECATTYPE", "ROLECATVAL"],
    },
    "ROLES": {
        "key": "role_id",
        "description": "Roles",
        "depends": [],
    },
    "RSRC": {
        "key": "rsrc_id",
        "description": "Resources",
        "depends": [],
    },
    "RSRCCURV": {
        "key": "curv_id",
        "description": "Resource Curves",
        "depends": [],
    },
    "RSRCCURVDATA": {
        "key": None,
        "description": "Resource Curve Data",
        "depends": ["RSRCCURV"],
    },
    "RSRCLEVELLIST": {
        "key": "rsrc_level_list_id",
        "description": "Resource Level List",
        "depends": ["RSRC"],
    },
    "RSRCRATE": {
        "key": "rsrc_rate_id",
        "description": "Resource Prices",
        "depends": ["RSRC"],
    },
    "RSRCRCAT": {
        "key": None,
        "description": "Resource Code Assignments",
        "depends": ["RCATVAL", "RCATTYPE", "RSRC"],
    },
    "RSRCROLE": {
        "key": None,
        "description": "Resource Role Assignments",
        "depends": ["ROLES", "RSRC"],
    },
    "SCHEDOPTIONS": {
        "key": "schedoptions_id",
        "description": "Schedule Options",
        "depends": [],
    },
    "SHIFT": {
        "key": "shift_id",
        "description": "Shift Names",
        "depends": [],
    },
    "SHIFTPER": {
        "key": "shift_period_id",
        "description": "Shifts",
        "depends": ["SHIFT"],
    },
    "TASK": {
        "key": "task_id",
        "description": "Activities",
        "depends": ["CALENDAR"],
    },
    "TASKACTV": {
        "key": None,
        "description": "Activity Code Assignments",
        "depends": ["ACTVCODE", "TASK"],
    },
    "TASKDOC": {
        "key": "taskdoc_id",
        "description": "Document Assignments",
        "depends": ["DOCUMENT", "TASK"],
    },
    "TASKFDBK": {
        "key": None,
        "description": "Activity Feedback",
        "depends": ["TASK"],
    },
    "TASKFIN": {
        "key": None,
        "description": "Activity Past Period Actuals",
        "depends": ["FINDATES", "TASK"],
    },
    "TASKMEMO": {
        "key": "memo_id",
        "description": "Activity Notebook",
        "depends": ["MEMOTYPE", "TASK"],
    },
    "TASKNOTE": {
        "key": None,
        "description": "Activity Notes to Resources",
        "depends": ["TASK"],
    },
    "TASKPRED": {
        "key": "task_pred_id",
        "description": "Activity Relationships",
        "depends": ["TASK"],
    },
    "TASKPROC": {
        "key": "proc_id",
        "description": "Activity Steps",
        "depends": ["TASK"],
    },
    "TASKRSRC": {
        "key": "taskrsrc_id",
        "description": "Activity Resource Assignments",
        "depends": ["RSRC", "TASK"],
    },
    "TASKUSER": {
        "key": None,
        "description": "Activity Owners",
        "depends": ["TASK"],
    },
    "THRSPARM": {
        "key": "thresh_parm_id",
        "description": "Threshold Parameters",
        "depends": [],
    },
    "TRSRCFIN": {
        "key": None,
        "description": "Activity Resource Assignment Past Period Actuals",
        "depends": ["FINDATES", "TASKRSRC"],
    },
    "UDFTYPE": {
        "key": "udf_type_id",
        "description": "User Defined Fields",
        "depends": [],
    },
    "UDFVALUE": {
        "key": None,
        "description": "User Defined Field Values",
        "depends": ["UDFTYPE"],
    },
    "UMEASURE": {
        "key": "unit_id",
        "description": "Units of Measure",
        "depends": [],
    },
    "WBSBUDG": {
        "key": "wbs_budg_id",
        "description": "Spending and Benefit Plans",
        "depends": [],
    },
    "WBSMEMO": {
        "key": "wbs_memo_id",
        "description": "EPS, Project and WBS Notebook",
        "depends": ["MEMOTYPE", "PROJWBS"],
    },
    "WBSSTEP": {
        "key": "wbs_step_id",
        "description": "WBS Milestones",
        "depends": [],
    },
}
