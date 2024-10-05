"""
- Application name: Dog's Dinner Constituent Calculator.
- Author: Dan Bright, dan@uplandsdynamic.com.
- Code hosted at: https://github.com/UplandsDynamic/dogs-dinner-constituent-calculator
- Description: 'Dry Matter Basis' calculation, 
   comparison & evaluation tool, for renal & pancreatitis 
   dog food diet suitability.
- Version: 0.2.4-beta
- License: GNU General Public License Version 3.0 (GPLv3.0),
   available at https://www.gnu.org/licenses/gpl-3.0.txt
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from copy import deepcopy

st.set_page_config(
    layout="wide", page_title="Dog's Dinner Constituent Calculator")

""" NON SESSION VARIABLES """

default_constituent_params = {
    'protein':
        {
            'desc': 'Protein',
            'measure_unit': '%',
            'panc': {
                'low': 20,
                'high': 30,
                'default_changed': False,
                'defaults': {
                    'low': 20,
                    'high': 30,
                }
            },
            'renal': {
                'low': 15,
                # changed from 30 (as per AADF) on 05/10/24 as other sites differ
                'high': 20,
                'default_changed': False,
                'defaults': {
                    'low': 15,
                    'high': 30,
                }
            },
        },
    'fat': {
            'desc': 'Fat',
            'measure_unit': '%',
            'panc': {
                'low': 5,
                'high': 10,
                'default_changed': False,
                'defaults': {
                    'low': 5,
                    'high': 10,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'carbs': {
            'desc': 'Carbohydrates',
            'measure_unit': '%',
            'panc': {
                'low': 0,
                'high': 60,
                'default_changed': False,
                'defaults': {
                    'low': 0,
                    'high': 60,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'fibre': {
            'desc': 'Fibre',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'sugar': {
            'desc': 'Added Sugars',
            'measure_unit': 'g',
            'panc': {
                'low': 0,
                'high': 0,
                'default_changed': False,
                'defaults': {
                    'low': 0,
                    'high': 0,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'sodium': {
            'desc': 'Sodium',
            'measure_unit': 'g/kcal',
            'panc': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
            'renal': {
                'low': 0.0004,
                'high': 0.0012,
                'default_changed': False,
                'defaults': {
                    'low': 0.0004,
                    'high': 0.0012,
                }
            },
        },
    'chloride': {
            'desc': 'Chloride',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'ash': {
            'desc': 'Ash',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
            'renal': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
        },
    'phosphorus': {
            'desc': 'Phosphorus',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
                'default_changed': False,
                'defaults': {
                    'low': None,
                    'high': None,
                }
            },
            'renal': {
                'low': 0.2,
                'high': 0.8,
                'default_changed': False,
                'defaults': {
                    'low': 0.2,
                    'high': 0.8,
                }
            },
        },
}

constituent_params = deepcopy(default_constituent_params)

""" SET VARIABLES IN SESSION STATE """

if "panc" not in st.session_state:
    st.session_state.panc = False
if "renal" not in st.session_state:
    st.session_state.renal = False
if "food_name" not in st.session_state:
    st.session_state.food_name = "Unnamed Food"
if "dm_fat" not in st.session_state:
    st.session_state.dm_fat = 0
if "dm_protein" not in st.session_state:
    st.session_state.dm_protein = 0
if "dm_carbs" not in st.session_state:
    st.session_state.dm_carbs = 0
if "dm_phosphorus" not in st.session_state:
    st.session_state.dm_phosphorus = 0
if "dm_sodium" not in st.session_state:
    st.session_state.dm_sodium = 0
if "dm_chloride" not in st.session_state:
    st.session_state.dm_chloride = 0
if "dm_fibre" not in st.session_state:
    st.session_state.dm_fibre = 0
if "dm_ash" not in st.session_state:
    st.session_state.dm_ash = 0
if "dm_salt" not in st.session_state:
    st.session_state.dm_salt = 0
if "dm_salt_measure_weight" not in st.session_state:
    st.session_state.dm_salt_measure_weight = 0
if "dm_sugar" not in st.session_state:
    st.session_state.dm_sugar = 0
if "dm_sugar_measure_weight" not in st.session_state:
    st.session_state.dm_sugar_measure_weight = 0
if "dm_kcal_per_g" not in st.session_state:
    st.session_state.dm_kcal_per_g = 0
if "dm_kcal_measure_weight" not in st.session_state:
    st.session_state.dm_kcal_measure_weight = 0
if "params_table_widget_key" not in st.session_state:
    st.session_state.params_table_widget_key = 0


""" FUNCTIONS """

# populate user input fields with example


def populate_example(example=False):
    st.session_state.default_inputs = {
        'food_name': 'Example Scrumptious Food' if example else '',
        'kcal': 90.0 if example else 0.0,
        'kcal_measure': 100.0 if example else 0.0,
        'moisture': 77.0 if example else 0.0,
        'protein': 6.3 if example else 0.0,
        'fibre': 0.4 if example else 0.0,
        'ash': 1.5 if example else 0.0,
        'fat': 2.0 if example else 0.0,
        'carbs': 0.0 if example else 0.0,
        'phosphorus': 0.2 if example else 0.0,
        'sodium': 0.06 if example else 0.0,
        'chloride': 0.4 if example else 0.0,
        'sugar': 0.0 if example else 0.0,
        'sugar_measure': 0.0 if example else 0.0,
        'salt': 0.0 if example else 0.0,
        'salt_measure': 0.0 if example else 0.0,
    }

# create editable parameter table


def gen_param_tables(constituent_params, key=st.session_state.params_table_widget_key):
    # callback that calls func to update the constituent params

    edited_constituent_params = {'panc': None, 'renal': None}
    with st.expander(':green[Click here to view or edit the calculation parameters.]'):
        st.write(
            'To adjust the calculation parameter(s), simple enter the new value(s) in the fields below.')
        tab_col_1, tab_col_2 = st.columns(2, gap="small")
        for condition in ('panc', 'renal',):
            with tab_col_1 if condition == 'panc' else tab_col_2:
                with st.container(border=True):
                    st.subheader(':blue[Pancreatitis Diet]' if condition ==
                                 'panc' else ':violet[Kidney Disease (Renal) Diet]')
                    data = pd.DataFrame.from_dict({
                        'min_dry_matter': {
                            x['desc']: x[condition]['low'] for x in constituent_params.values() if x.get(condition).get('low', None) is not None and x.get(condition).get('high', None) is not None
                        },
                        'max_dry_matter': {
                            x['desc']: x[condition]['high'] for x in constituent_params.values() if x.get(condition).get('low', None) is not None and x.get(condition).get('high', None) is not None
                        },
                        'measure_unit': {
                            x['desc']: x['measure_unit'] for x in constituent_params.values() if x.get(condition).get('low', None) is not None and x.get(condition).get('high', None) is not None
                        },
                    })
                    edited_constituent_params[condition] = pd.DataFrame.to_dict(
                        st.data_editor(
                            data,
                            column_config={
                                'min_dry_matter': st.column_config.NumberColumn(
                                    label="Minimum Dry Matter",
                                ),
                                'max_dry_matter': st.column_config.NumberColumn(
                                    label="Maximum Dry Matter",
                                ),
                                'measure_unit': st.column_config.TextColumn(
                                    label="Measure Unit",
                                )
                            },
                            disabled=['', 'measure_unit'],
                            key=f"""state_{key}_{
                                condition}_constituent_param_editor""",
                            use_container_width=True,
                        )
                    )

        st.button(':orange[Restore Defaults]',
                  on_click=reset_constituent_params)
        update_constituent_params(
            constituent_params, edited_constituent_params)

# function to reset the constituent params


def reset_constituent_params():
    st.session_state.params_table_widget_key = 1 if not st.session_state.params_table_widget_key else 0

# function to update the constituent params upon user edit


def update_constituent_params(constituent_params, edited_constituent_params):
    if constituent_params and edited_constituent_params:
        for condition, data in edited_constituent_params.items():
            for k, v in data.items():
                if k == 'min_dry_matter':
                    {constituent_params[a][condition].update({'low': y, 'default_changed': True}) for x, y in v.items()
                        for a, b in constituent_params.items() if b.get('desc') == x if constituent_params[a][condition]['low'] != y}
                elif k == 'max_dry_matter':
                    {constituent_params[a][condition].update({'high': y, 'default_changed': True}) for x, y in v.items()
                        for a, b in constituent_params.items() if b.get('desc') == x if constituent_params[a][condition]['high'] != y}


# calculate dry matter fat (%)


@st.cache_data
def calc_fat(fat, moisture):
    return (fat / (100-moisture)) * 100

# calculate dry matter protein (%)


@st.cache_data
def calc_protein(protein, moisture):
    return (protein / (100-moisture)) * 100

# calculate dry matter carbohydrate (%)


def calc_carbs(carbs, dm_fat, dm_protein, dm_fibre, dm_ash, moisture):
    dm_non_carbs = dm_fat + dm_protein + dm_fibre + dm_ash
    return ((carbs / (100-moisture)) * 100) if carbs else (100 - dm_non_carbs) if dm_non_carbs <= 100 else 0

# calculate dry matter fibre (%)


@st.cache_data
def calc_fibre(fibre, moisture):
    return (fibre / (100-moisture)) * 100

# calculate dry matter ash (%)


@st.cache_data
def calc_ash(ash, moisture):
    return (ash / (100-moisture)) * 100

# calculate dry matter phosphorus (%)


@st.cache_data
def calc_phosphorus(phosphorus, moisture):
    return (phosphorus / (100-moisture)) * 100

# calculate dry matter sodium (%)


@st.cache_data
def calc_sodium(sodium, salt, salt_measure_weight, moisture):
    return ((sodium + ((salt * 0.4) / salt_measure_weight * 100 if salt_measure_weight else 0)) / (100-moisture)) * 100

# calculate dry matter chloride (%)


@st.cache_data
def calc_chloride(chloride, salt, salt_measure_weight, moisture):
    return ((chloride + ((salt * 0.6) / salt_measure_weight * 100 if salt_measure_weight else 0)) / (100-moisture)) * 100

# calculate dry matter sugar (%)


@st.cache_data
def calc_sugar(sugar, sugar_measure_weight, moisture):
    return ((sugar / sugar_measure_weight * 100) / (100-moisture)) * 100

# calculate dry matter in the weight of 'as fed' food provided as a base for kcal/salt/sugar ratios (g)


@st.cache_data
def calc_kcal_measure_weight(kcal_measure_weight, moisture):
    return kcal_measure_weight * ((100-moisture) / 100)

# calculate kcal per dry matter gram (g) (can assume moisture has 0 calories)


@st.cache_data
def calc_kcal_per_g(kcal, kcal_measure_weight, moisture):
    return kcal / (kcal_measure_weight * ((100-moisture) / 100))


# function to create pie chart


def create_pie(nutrients):
    sorted_nutrients = {k: v for k, v in sorted(
        nutrients.items(), key=lambda item: item[1], reverse=True)}
    labels = [k for k, _ in sorted_nutrients.items()]
    wedge_sizes = [v for v in sorted_nutrients.values()]
    if all(x > 0 for x in wedge_sizes):  # only draw if all nutrients above 0
        # to explode a wedge, change to 0.1
        explode = tuple((0 for _ in range(len(labels))))
        plt.figure(facecolor='none')
        wedges, _, _ = plt.pie(wedge_sizes, explode=explode, labels=labels, autopct='',
                               shadow=False, startangle=180, labeldistance=1.2, textprops={'color': 'white', 'size': 12})
        legend_labels = [
            f'{label} ({size:.2f}%)' for label, size in zip(labels, wedge_sizes)]
        plt.legend(wedges, legend_labels, loc="lower center",
                   bbox_to_anchor=(0.5, -0.6), fontsize=12, title="Legend")
        plt.axis('equal')  # Equal aspect ratio ensures circle.
        st.pyplot(plt)

# function to create bar chart


def create_bar_chart(data):
    df = pd.DataFrame.from_dict(data, orient='index').reset_index()
    df.columns = ['Nutrient', 'Percentage']
    df_sorted = df.sort_values(by='Percentage', ascending=False)
    df_sorted = df_sorted[df_sorted['Percentage'] != 0]
    chart = alt.Chart(df_sorted).mark_bar().encode(
        x=alt.X('Nutrient', sort=alt.EncodingSortField(
            field='Percentage', order='descending')),
        y=alt.Y('Percentage', scale=alt.Scale(
            type='linear', domain=(0, df_sorted.iloc[0]['Percentage'])))).configure_axis(labelLimit=0, labelFontSize=14)
    st.altair_chart(chart, use_container_width=True)

# function to display the metrics in charts


def display_charts(constituent_params, fat, fibre, protein, carbs, ash, phosphorus, chloride, sodium, sugar):
    st.subheader(":grey[Macronutrient Proportion Breakdown]")
    pie_params = {
        constituent_params['fat']['desc']: fat,
        constituent_params['protein']['desc']: protein,
        constituent_params['carbs']['desc']: carbs,
        constituent_params['fibre']['desc']: fibre,
        constituent_params['ash']['desc']: ash,
    }
    if fat and fibre and protein and ash:
        create_pie({k: v for k, v in pie_params.items() if v})
    else:
        st.markdown("Insufficient data to display")
    st.divider()
    st.subheader(":grey[Macronutrient Percentages]")
    if fat or fibre or protein:
        create_bar_chart({k: v for k, v in pie_params.items() if v})
    else:
        st.markdown("Insufficient data to display")

    st.subheader(":grey[Micronutrient Percentages]")

    if phosphorus or sodium or chloride:
        create_bar_chart({constituent_params['phosphorus']['desc']: phosphorus,
                          constituent_params['sodium']['desc']: sodium,
                          constituent_params['chloride']['desc']: chloride,
                          constituent_params['sugar']['desc']: sugar})
    else:
        st.markdown("Insufficient data to display")

# function to ensure metrics required for calculations have been submitted


def enforce_required(kcal_measure_weight, kcal, salt, salt_measure_weight,
                     sugar, sugar_measure_weight, protein, fibre, fat, ash,
                     sodium, phosphorus, moisture):
    test_passed = True
    if not kcal_measure_weight or not kcal:
        st.warning(
            f":blue[Both the Calories (kcal) and 'per weight of food (g)' fields need to be provided.]")
        test_passed = False
    if salt and not salt_measure_weight:
        st.warning(
            ':blue[If salt is given, the *per grams* field needs to be provided.]')
        test_passed = False
    if sugar and not sugar_measure_weight:
        st.warning(
            ':blue[If sugar is given, the *per grams* field needs to be provided.]')
        test_passed = False
    if not protein:
        st.warning(
            f':blue[A value for protein needs to be provided.]')
        test_passed = False
    if not fibre:
        st.warning(
            f':blue[A value for fibre needs to be provided.]')
        test_passed = False
    if not fat:
        st.warning(
            f':blue[A value for fat needs to be provided.]')
        test_passed = False
    if not ash:
        st.warning(
            f':blue[A value for ash needs to be provided.]')
        test_passed = False
    if not sodium:
        st.warning(
            f':blue[A value for sodium needs to be provided.]')
        test_passed = False
    if not phosphorus:
        st.warning(
            f':blue[A value for phosphorus needs to be provided.]')
        test_passed = False
    if not moisture:
        st.warning(
            f':blue[A value for moisture needs to be provided.]')
        test_passed = False
    if protein + fibre + fat + ash + sodium + phosphorus + moisture > 100:
        st.error(
            f':blue[The crude values you input for protein, fibre, fat, ash, sodium, phosphorus and moisture total in excess of 100%. Please amend before continuing.]')
        test_passed = False
    return test_passed

# function to run pancreatitis tests


def run_panc_tests(constituent_params, dm_fat, dm_protein, dm_carbs, dm_sugar):
    result = []
    # test fat
    if dm_fat >= constituent_params['fat']['panc']['low'] and dm_fat <= constituent_params['fat']['panc']['high']:
        result.append({'nutrient': constituent_params['fat']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['fat']['panc']['default_changed'],
                       'defaults': constituent_params['fat']['panc']['defaults'],
                       })
    elif dm_fat < constituent_params['fat']['panc']['low']:
        result.append({'nutrient': constituent_params['fat']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['fat']['panc']['low'] - dm_fat,
                       'delta_pc': (((constituent_params['fat']['panc']['low'] - dm_fat) / dm_fat) * 100) if dm_fat else 100,
                       'default_param_changed': constituent_params['fat']['panc']['default_changed'],
                       'defaults': constituent_params['fat']['panc']['defaults'],
                       })
    elif dm_fat > constituent_params['fat']['panc']['high']:
        result.append({'nutrient': constituent_params['fat']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_fat - constituent_params['fat']['panc']['high'],
                       'delta_pc': (((dm_fat - constituent_params['fat']['panc']['high']) / constituent_params['fat']['panc']['high']) * 100 if constituent_params['fat']['panc']['high'] else 100),
                       'default_param_changed': constituent_params['fat']['panc']['default_changed'],
                       'defaults': constituent_params['fat']['panc']['defaults'],
                       })
    #  test protein
    if dm_protein >= constituent_params['protein']['panc']['low'] and dm_protein <= constituent_params['protein']['panc']['high']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['protein']['panc']['default_changed'],
                       'defaults': constituent_params['protein']['panc']['defaults'],
                       })
    elif dm_protein < constituent_params['protein']['panc']['low']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['protein']['panc']['low'] - dm_protein,
                       'delta_pc': (((constituent_params['protein']['panc']['low'] - dm_protein) / dm_protein) * 100) if dm_protein else 100,
                       'default_param_changed': constituent_params['protein']['panc']['default_changed'],
                       'defaults': constituent_params['protein']['panc']['defaults'],
                       })
    elif dm_protein > constituent_params['protein']['panc']['high']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_protein - constituent_params['protein']['panc']['high'],
                       'delta_pc': (((dm_protein - constituent_params['protein']['panc']['high']) / constituent_params['protein']['panc']['high']) * 100) if constituent_params['protein']['panc']['high'] else 100,
                       'default_param_changed': constituent_params['protein']['panc']['default_changed'],
                       'defaults': constituent_params['protein']['panc']['defaults'],
                       })
    #  test carbs
    if dm_carbs >= constituent_params['carbs']['panc']['low'] and dm_carbs <= constituent_params['carbs']['panc']['high']:
        result.append({'nutrient': constituent_params['carbs']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['carbs']['panc']['default_changed'],
                       'defaults': constituent_params['carbs']['panc']['defaults'],
                       })
    elif dm_carbs < constituent_params['carbs']['panc']['low']:
        result.append({'nutrient': constituent_params['carbs']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['carbs']['panc']['low'] - dm_carbs,
                       'delta_pc': (((constituent_params['carbs']['panc']['low'] - dm_carbs) / dm_carbs) * 100) if dm_carbs else 100,
                       'default_param_changed': constituent_params['carbs']['panc']['default_changed'],
                       'defaults': constituent_params['carbs']['panc']['defaults'],
                       })
    elif dm_carbs > constituent_params['carbs']['panc']['high']:
        result.append({'nutrient': constituent_params['carbs']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_carbs - constituent_params['carbs']['panc']['high'],
                       'delta_pc': (((dm_carbs - constituent_params['carbs']['panc']['high']) / constituent_params['carbs']['panc']['high']) * 100) if constituent_params['carbs']['panc']['high'] else 100,
                       'default_param_changed': constituent_params['carbs']['panc']['default_changed'],
                       'defaults': constituent_params['carbs']['panc']['defaults'],
                       })
    # test sugar
    if dm_sugar >= constituent_params['sugar']['panc']['low'] and dm_sugar <= constituent_params['sugar']['panc']['high']:
        result.append({'nutrient': constituent_params['sugar']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['sugar']['panc']['default_changed'],
                       'defaults': constituent_params['sugar']['panc']['defaults'],
                       })
    elif dm_sugar < constituent_params['sugar']['panc']['low']:
        result.append({'nutrient': constituent_params['sugar']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['sugar']['panc']['low'] - dm_sugar,
                       'delta_pc': (((constituent_params['sugar']['panc']['low'] - dm_sugar) / dm_sugar) * 100) if dm_sugar else 100,
                       'default_param_changed': constituent_params['sugar']['panc']['default_changed'],
                       'defaults': constituent_params['sugar']['panc']['defaults'],
                       })
    elif dm_sugar > constituent_params['sugar']['panc']['high']:
        result.append({'nutrient': constituent_params['sugar']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_sugar - constituent_params['sugar']['panc']['high'],
                       'delta_pc': (((dm_sugar - constituent_params['sugar']['panc']['high']) / constituent_params['sugar']['panc']['high']) * 100) if constituent_params['sugar']['panc']['high'] else 100,
                       'default_param_changed': constituent_params['sugar']['panc']['default_changed'],
                       'defaults': constituent_params['sugar']['panc']['defaults'],
                       })
    return result

# function to run renal tests


def run_renal_tests(constituent_params, dm_phosphorus, dm_protein, dm_sodium, dm_kcal_per_g):
    result = []
    # test phosphorus
    if dm_phosphorus >= constituent_params['phosphorus']['renal']['low'] and dm_phosphorus <= constituent_params['phosphorus']['renal']['high']:
        result.append({'nutrient': constituent_params['phosphorus']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['phosphorus']['renal']['default_changed'],
                       'defaults': constituent_params['phosphorus']['renal']['defaults'],
                       })
    elif dm_phosphorus < constituent_params['phosphorus']['renal']['low']:
        result.append({'nutrient': constituent_params['phosphorus']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['phosphorus']['renal']['low'] - dm_phosphorus,
                       'delta_pc': (((constituent_params['phosphorus']['renal']['low'] - dm_phosphorus) / dm_phosphorus) * 100) if dm_phosphorus else 100,
                       'unit': '%',
                       'default_param_changed': constituent_params['phosphorus']['renal']['default_changed'],
                       'defaults': constituent_params['phosphorus']['renal']['defaults'],
                       })
    elif dm_phosphorus > constituent_params['phosphorus']['renal']['high']:
        result.append({'nutrient': constituent_params['phosphorus']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_phosphorus - constituent_params['phosphorus']['renal']['high'],
                       'delta_pc': (((dm_phosphorus - constituent_params['phosphorus']['renal']['high']) / constituent_params['phosphorus']['renal']['high']) * 100) if constituent_params['phosphorus']['renal']['high'] else 100,
                       'unit': '%',
                       'default_param_changed': constituent_params['phosphorus']['renal']['default_changed'],
                       'defaults': constituent_params['phosphorus']['renal']['defaults'],
                       })
    #  test protein
    if dm_protein >= constituent_params['protein']['renal']['low'] and dm_protein <= constituent_params['protein']['renal']['high']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': True,
                       'reason': None,
                       'default_param_changed': constituent_params['protein']['renal']['default_changed'],
                       'defaults': constituent_params['protein']['renal']['defaults'],
                       })
    elif dm_protein < constituent_params['protein']['renal']['low']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': constituent_params['protein']['renal']['low'] - dm_protein,
                       'delta_pc': (((constituent_params['protein']['renal']['low'] - dm_protein) / dm_protein) * 100) if dm_protein else 100,
                       'unit': '%',
                       'default_param_changed': constituent_params['protein']['renal']['default_changed'],
                       'defaults': constituent_params['protein']['renal']['defaults'],
                       })
    elif dm_protein > constituent_params['protein']['renal']['high']:
        result.append({'nutrient': constituent_params['protein']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_protein - constituent_params['protein']['renal']['high'],
                       'delta_pc': (((dm_protein - constituent_params['protein']['renal']['high']) / constituent_params['protein']['renal']['high']) * 100) if constituent_params['protein']['renal']['high'] else 100,
                       'unit': '%',
                       'default_param_changed': constituent_params['protein']['renal']['default_changed'],
                       'defaults': constituent_params['protein']['renal']['defaults'],
                       })
    # test sodium
    dm_food_g_per_kcal = 1 / dm_kcal_per_g
    dm_sodium_g_per_kcal = dm_food_g_per_kcal * \
        (dm_sodium / 100) if dm_sodium else 0
    if dm_sodium_g_per_kcal >= constituent_params['sodium']['renal']['low'] and dm_sodium_g_per_kcal <= constituent_params['sodium']['renal']['high']:
        result.append(
            {'nutrient': constituent_params['sodium']['desc'],
                'pass': True,
                'reason': None,
                'default_param_changed': constituent_params['sodium']['renal']['default_changed'],
                'defaults': constituent_params['sodium']['renal']['defaults'],
             })
    elif dm_sodium_g_per_kcal < constituent_params['sodium']['renal']['low']:
        result.append(
            {'nutrient': constituent_params['sodium']['desc'],
                'pass': False,
                'reason': 'low',
                'delta': constituent_params['sodium']['renal']['low'] - dm_sodium_g_per_kcal,
                'delta_pc': (((constituent_params['sodium']['renal']['low'] - dm_sodium_g_per_kcal) / dm_sodium_g_per_kcal) * 100) if dm_sodium_g_per_kcal else 100,
                'unit': 'g/kcal',
                'default_param_changed': constituent_params['sodium']['renal']['default_changed'],
                'defaults': constituent_params['sodium']['renal']['defaults'],
             })
    elif dm_sodium_g_per_kcal > constituent_params['sodium']['renal']['high']:
        result.append(
            {'nutrient': constituent_params['sodium']['desc'],
                'pass': False,
                'reason': 'high',
                'delta': dm_sodium_g_per_kcal - constituent_params['sodium']['renal']['high'],
                'delta_pc': (((dm_sodium_g_per_kcal - constituent_params['sodium']['renal']['low']) / constituent_params['sodium']['renal']['low']) * 100) if constituent_params['sodium']['renal']['high'] else 100,
                'unit': 'g/kcal',
                'default_param_changed': constituent_params['sodium']['renal']['default_changed'],
                'defaults': constituent_params['sodium']['renal']['defaults'],
             })
    return result

#  function to display calculations


def display_calculations(constituent_params, fat, protein, carbs, fibre, ash, phosphorus, sodium, chloride, sugar, kcal_per_g):
    dry_matter_stats_df = pd.DataFrame.from_dict([{
        constituent_params['fat']['desc']: fat,
        constituent_params['protein']['desc']: protein,
        constituent_params['carbs']['desc']: carbs,
        constituent_params['fibre']['desc']: fibre,
        constituent_params['ash']['desc']: ash,
        constituent_params['phosphorus']['desc']: phosphorus,
        constituent_params['sodium']['desc']: sodium,
        constituent_params['chloride']['desc']: chloride,
        constituent_params['sugar']['desc']: sugar}])
    dry_matter_stats_df = pd.melt(dry_matter_stats_df,
                                  var_name='Dry Matter Constituent',
                                  value_name='Value (%)',
                                  ignore_index=True)
    dry_matter_stats_df.dropna(inplace=True)
    with st.container(border=True):
        st.markdown(f'Calories per dry matter gram (kcal): {kcal_per_g:.2f}')
    st.dataframe(
        dry_matter_stats_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            'Value': st.column_config.NumberColumn(
                'Value',
                format='%.2f %%'
            )
        })

# function to display results


def display_results(food_name, panc, renal):
    # pancreatitis diet
    with st.container(border=True):
        st.subheader(':blue[Pancreatitis Diet]')
        if all(d.get('pass', False) == True for d in panc):
            st.success(
                f'''{food_name} is suitable for a pancreatitis diet''', icon='👍')
            if any(d.get('default_param_changed') for d in panc):
                st.warning(f"""Warning: The default calculation parameters have been
                        changed for the following constituents: {', '.join([
                    d['nutrient'] for d in panc if d.get('default_param_changed')])}""")
        else:
            st.error(f'''{food_name} is unsuitable for dogs with pancreatitis.''',
                     icon='👎')
            for test in panc:
                if test['pass'] == False:
                    delta_pc = round(
                        test['delta_pc'], 2) if test['delta_pc'] <= 100 else 'over 100'
                    st.markdown(f"""{test['nutrient']} is {delta_pc}% too {
                                test['reason']}""", help="""Percentage indicates the difference between the constituent amount and the recommendation. For example, "100% too high" would mean the food contained twice as much that constituent as would be appropriate for that diet.""")
    # renal diet
    with st.container(border=True):
        st.subheader(':violet[Renal Diet]')
        if all(d.get('pass', False) == True for d in renal):
            st.success(
                f'''{food_name} is suitable for a renal diet''', icon='👍')
            if any(d.get('default_param_changed') for d in renal):
                st.warning(f"""Warning: The default calculation parameters have been
                        changed for the following constituents: {', '.join([
                    d['nutrient'] for d in renal if d.get('default_param_changed')])}""")
        else:
            st.error(f'''{food_name} is unsuitable for dogs with kidney disease.''',
                     icon='👎')
            for test in renal:
                if test['pass'] == False:
                    delta_pc = round(
                        test['delta_pc'], 2) if test['delta_pc'] <= 100 else 'over 100'
                    st.markdown(f"""{test['nutrient']} is {delta_pc}% too {test['reason']}""", help="""Percentage indicates the *proportional difference* between the constituent amount and the recommendation. For example, "100% too high" would mean the food contains *twice* as much of that constituent as would be appropriate for the diet.\n\nNote that the figure does not refer to the *crude difference* in actual percentages between the food and the recommendation (e.g., if the recommended value is 12%, but the actual value is 15%, the *crude difference* would be 12-3 = 3%, but the *proportional difference* (as used in this metric) would be 15/12 = 1.25, which is to say 15% is 25% greater than the recommended value of 12%).""")


""" PAGE 1 """
header_col_1, header_col_2 = st.columns([15, 85], gap='medium')
with st.container():
    with header_col_1:
        with st.container(border=True):
            st.image('logo.jpg', use_column_width=True)
    with header_col_2:
        with st.container(border=False):
            st.title(":rainbow[Dog's Dinner Constituent Calculator]")
            st.header(
                ":grey[Dry Matter Basis Calculator for Renal & Pancreatitis Diets]", divider=False)
with st.container(border=True):
    st.subheader(":grey[About]")
    st.warning('This app is currently in beta testing, therefore the results may be inaccurate. Please do not rely solely on the information provided here.', icon="ℹ️")
    st.markdown("The purpose of this calculator is to provide 'Dry Matter Basis' comparison between commercially available dog foods, where the 'analytical constituents' are provided by the manufacturer 'As Fed'.\n\nBased on this information, the app also indicates the food's suitability as a diet for dogs with kidney (renal) disease, and/or pancreatitis.")
    with st.expander(':green[Click here to expand details about what this app does, and why it does it.]'):
        st.markdown(
            """Converting the 'As Fed' constituent measures to a 'Dry Matter Basis' basis allows for a more accurate comparison between wet and dry foods.\n\nFor more details about what 'Dry Matter Basis' is, why it matters, and how it is calculated, please refer to the [All About Dog Food<sup>1</sup>](https://www.allaboutdogfood.co.uk/dog-food-terms/0013/dry-matter-nutrients) website.\n\nSpecifically, this calculator assesses the suitability of the food constituents for dogs with kidney disease (requiring a renal diet), and for dogs with disease of the pancreas (requiring a pancreatitis diet).\n\nDefault values for the calculations used to establish the suitability of the dog food constituents are based mainly on the information provided by the [All About Dog Food<sup>2</sup>](https://allaboutdogfood.co.uk) and [PetMD<sup>3</sup>](https://www.petmd.com/dog/nutrition/what-feed-dog-kidney-disease) websites.""", unsafe_allow_html=True)
        st.caption("""<sup>(1,2,3)</sup> This app has no affiliation with the 'All About Dog Food' or 'PetMD' websites.""",
                   unsafe_allow_html=True)

with st.container(border=True):
    st.subheader(":grey[Calculation Parameters]")
    st.markdown(
        """The default parameters for the calculations are currently set largely with reference to the information published at [All About Dog Food](https://www.allaboutdogfood.co.uk).""")

    gen_param_tables(constituent_params)

col_1, col_2, col_3 = st.columns(3, gap="medium")
with col_1:
    with st.container(border=True):
        st.subheader(":grey[Food Content 'As Fed']", divider="red")
        button_col_1,  button_col_2 = st.columns(2, gap='small')
        with button_col_1:
            st.button('Fill With Example', use_container_width=True,
                      on_click=populate_example, args=[True]),
        with button_col_2:
            st.button('Reset Values', use_container_width=True,
                      on_click=populate_example, args=[False])

        # input form

        if "default_inputs" not in st.session_state:
            populate_example(False)

        st.session_state.food_name = st.text_input(
            label="Food name", value=st.session_state.default_inputs['food_name']
        )

        with st.container(border=True):
            cal_col_1, cal_col_2 = st.columns(2)
            with cal_col_1:
                st.session_state.crude_kcal = st.number_input(
                    label="Calories (kcal)", key='kcal', min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['kcal']
                )
            with cal_col_2:
                st.session_state.crude_kcal_measure_weight = st.number_input(
                    label="per weight of food (g)", key='kcal_measure_weight', min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['kcal_measure']
                )

        st.session_state.crude_moisture = st.number_input(
            label="Moisture Content (%)", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['moisture'],
            help="If moisture content is not listed for dry foods, it may be estimated to be around 10%."
        )

        st.session_state.crude_fat = st.number_input(
            label=f"Crude {constituent_params['fat']['desc']} ({constituent_params['fat']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['fat'],
        )

        st.session_state.crude_protein = st.number_input(
            label=f"Crude {constituent_params['protein']['desc']} ({constituent_params['protein']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['protein'],
        )

        st.session_state.crude_carbs = 0.0
        """
        # Allow app to calculate carbs based on remainder after other inputs. 
        # To enable user input, uncomment this block.
        st.session_state.crude_carbs = st.number_input(
            label=f"Crude {constituent_params['carbs']['desc']} ({constituent_params['carbs']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['carbs'],
            help="If a value for carbohydrates is not available, this will be estimated for the calculations as the remainder of 'dry matter' food after accounting for protein, fat, fibre and ash."
        )"""

        st.session_state.crude_fibre = st.number_input(
            label=f"Crude {constituent_params['fibre']['desc']} ({constituent_params['fibre']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['fibre'],
        )

        st.session_state.crude_ash = st.number_input(
            label=f"{constituent_params['ash']['desc']} ({constituent_params['ash']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['ash'],
            help="""Ash may also be referred to as 'inorganic matter' or 'incinerated matter'. It contains mineral nutrients that are beneficial for the dog's health. For more information, see [this page on the Dog Food Advisor website](https://www.dogfoodadvisor.com/choosing-dog-food/dog-food-ash/)."""
        )

        st.session_state.crude_phosphorus = st.number_input(
            label=f"{constituent_params['phosphorus']['desc']} ({constituent_params['phosphorus']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['phosphorus'],
        )

        st.session_state.crude_sodium = st.number_input(
            label=f"{constituent_params['sodium']['desc']} ({constituent_params['sodium']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['sodium'],
        )

        st.session_state.crude_chloride = st.number_input(
            label=f"{constituent_params['chloride']['desc']} ({constituent_params['chloride']['measure_unit']})", min_value=0.00, max_value=100.0, value=st.session_state.default_inputs['chloride'],
        )

        with st.container(border=True):
            salt_col_1, salt_col_2 = st.columns(2)
            with salt_col_1:
                st.session_state.crude_salt = st.number_input(
                    label="Added Salt (g)", key='salt', min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['salt_measure'],
                    help="Added salt is assumed to be composed of 40% Sodium and 60% Chloride, as referenced in the [European Union's Knowledge for Policy documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en)"
                )
            with salt_col_2:
                st.session_state.crude_salt_measure_weight = st.number_input(
                    label="per weight of food (g)", key="salt_measure_weight", min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['salt_measure']
                )

        with st.container(border=True):
            sugar_col_1, sugar_col_2 = st.columns(2)
            with sugar_col_1:
                st.session_state.crude_sugar = st.number_input(
                    label=f"{constituent_params['sugar']['desc']} ({constituent_params['sugar']['measure_unit']})", key='sugar', min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['sugar']
                )
            with sugar_col_2:
                st.session_state.crude_sugar_measure_weight = st.number_input(
                    label="per weight of food (g)", key="sugar_measure_weight", min_value=0.00, max_value=100000.0, value=st.session_state.default_inputs['sugar_measure']
                )
with col_2:
    with st.container(border=True):
        st.subheader(":grey[Dry Matter Basis (Results)]", divider="red")
        # check input
        required_satisfied = enforce_required(
            kcal_measure_weight=st.session_state.crude_kcal_measure_weight,
            kcal=st.session_state.crude_kcal,
            salt=st.session_state.crude_salt,
            salt_measure_weight=st.session_state.crude_salt_measure_weight,
            sugar=st.session_state.crude_sugar,
            sugar_measure_weight=st.session_state.crude_sugar_measure_weight,
            protein=st.session_state.crude_protein,
            fat=st.session_state.crude_fat,
            fibre=st.session_state.crude_fibre,
            ash=st.session_state.crude_ash,
            sodium=st.session_state.crude_sodium,
            phosphorus=st.session_state.crude_phosphorus,
            moisture=st.session_state.crude_moisture,
        )
        # run the calculations
        if required_satisfied:
            st.session_state.dm_fat = round(
                calc_fat(st.session_state.crude_fat, st.session_state.crude_moisture), 3)
            st.session_state.dm_protein = round(
                calc_protein(st.session_state.crude_protein, st.session_state.crude_moisture), 3)
            st.session_state.dm_fibre = round(
                calc_fibre(st.session_state.crude_fibre, st.session_state.crude_moisture), 3)
            st.session_state.dm_ash = round(
                calc_ash(st.session_state.crude_ash, st.session_state.crude_moisture), 3)
            st.session_state.dm_carbs = round(
                # carbs has to be below fat, protein, fibre & ash
                calc_carbs(st.session_state.crude_carbs,
                           st.session_state.dm_fat,
                           st.session_state.dm_protein,
                           st.session_state.dm_fibre,
                           st.session_state.dm_ash,
                           st.session_state.crude_moisture), 3)
            st.session_state.dm_phosphorus = round(
                calc_phosphorus(st.session_state.crude_phosphorus, st.session_state.crude_moisture), 3)
            st.session_state.dm_sodium = round(
                calc_sodium(st.session_state.crude_sodium, st.session_state.crude_salt, st.session_state.crude_salt_measure_weight, st.session_state.crude_moisture), 3)
            st.session_state.dm_chloride = round(
                calc_chloride(st.session_state.crude_chloride, st.session_state.crude_salt, st.session_state.crude_salt_measure_weight, st.session_state.crude_moisture), 3)
            st.session_state.dm_sugar = round(
                calc_sugar(st.session_state.crude_sugar, st.session_state.crude_sugar_measure_weight, st.session_state.crude_moisture) if st.session_state.crude_sugar and st.session_state.crude_sugar_measure_weight else 0, 3)
            st.session_state.dm_kcal_per_g = round(
                calc_kcal_per_g(st.session_state.crude_kcal, st.session_state.crude_kcal_measure_weight, st.session_state.crude_moisture), 3)
            st.session_state.dm_kcal_measure_weight = round(
                calc_kcal_measure_weight(st.session_state.crude_kcal_measure_weight, st.session_state.crude_moisture), 3)
            # display output
            display_calculations(
                constituent_params=constituent_params,
                ash=st.session_state.dm_ash,
                fat=st.session_state.dm_fat,
                protein=st.session_state.dm_protein,
                carbs=st.session_state.dm_carbs,
                sugar=st.session_state.dm_sugar,
                fibre=st.session_state.dm_fibre,
                phosphorus=st.session_state.dm_phosphorus,
                sodium=st.session_state.dm_sodium,
                chloride=st.session_state.dm_chloride,
                kcal_per_g=st.session_state.dm_kcal_per_g)
            st.divider()
            # display metrics in charts
            display_charts(
                constituent_params=constituent_params,
                ash=st.session_state.dm_ash,
                fat=st.session_state.dm_fat,
                protein=st.session_state.dm_protein,
                carbs=st.session_state.dm_carbs,
                sugar=st.session_state.dm_sugar,
                fibre=st.session_state.dm_fibre,
                phosphorus=st.session_state.dm_phosphorus,
                sodium=st.session_state.dm_sodium,
                chloride=st.session_state.dm_chloride)
with col_3:
    with st.container(border=True):
        st.subheader(":grey[Diet Suitability]", divider="red")
        if required_satisfied:
            # run tests & display results (provided calories have been entered; essential for calculations)
            if st.session_state.dm_kcal_per_g:
                st.session_state.panc = run_panc_tests(
                    constituent_params=constituent_params,
                    dm_fat=st.session_state.dm_fat,
                    dm_protein=st.session_state.dm_protein,
                    dm_carbs=st.session_state.dm_carbs,
                    dm_sugar=st.session_state.dm_sugar)
                st.session_state.renal = run_renal_tests(
                    constituent_params=constituent_params,
                    dm_phosphorus=st.session_state.dm_phosphorus,
                    dm_protein=st.session_state.dm_protein,
                    dm_sodium=st.session_state.dm_sodium,
                    dm_kcal_per_g=st.session_state.dm_kcal_per_g)
                # display results
                display_results(food_name=st.session_state.food_name if st.session_state.food_name else "This food",
                                panc=st.session_state.panc,
                                renal=st.session_state.renal)

with st.container(border=True):
    st.subheader(":grey[References]")
    st.markdown(
        "[All About Dog Food](https://www.allaboutdogfood.co.uk) (Web Resource)")
    st.markdown(
        "[Dog Food Advisor](https://www.dogfoodadvisor.com/choosing-dog-food/dog-food-ash/) (Web Resource)")
    st.markdown("[European Union's Knowledge for Policy Documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en) (Official Documentation)")
    st.markdown("[PedMD: What to feed a dog with kidney disease](https://www.petmd.com/dog/nutrition/what-feed-dog-kidney-disease) (Web Resource)")

st.caption('App developed by [Dan Bright (UplandsDynamic)](mailto:dan@uplandsdynamic.com). Version: 0.2.2-beta. Code available on [GitHub](https://github.com/uplandsdynamic/dogs-dinner-constituent-calculator). Licensed GPLv3.')
