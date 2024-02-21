import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")

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

""" FUNCTIONS """

# function to define calculation parameters


@st.cache_data
def get_constituent_params():
    return {
        'protein':
        {
            'desc': 'Protein',
            'measure_unit': '%',
            'panc': {
                'low': 20,
                'high': 30,
            },
            'renal': {
                'low': 15,
                'high': 30,
            },
        },
        'fat': {
            'desc': 'Fat',
            'measure_unit': '%',
            'panc': {
                'low': 5,
                'high': 10,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'carbs': {
            'desc': 'Carbohydrates',
            'measure_unit': '%',
            'panc': {
                'low': 0,
                'high': 60,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'fibre': {
            'desc': 'Fibre',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'sugar': {
            'desc': 'Added Sugars',
            'measure_unit': 'g',
            'panc': {
                'low': 0,
                'high': 0,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'sodium': {
            'desc': 'Sodium',
            'measure_unit': 'g/kcal',
            'panc': {
                'low': None,
                'high': None,
            },
            'renal': {
                'low': 0.0004,
                'high': 0.0012,
            },
        },
        'chloride': {
            'desc': 'Chloride',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'ash': {
            'desc': 'Ash',
            'measure_unit': '%',
            'panc': {
                    'low': None,
                    'high': None,
            },
            'renal': {
                'low': None,
                'high': None,
            },
        },
        'phosphorus': {
            'desc': 'Phosphorus',
            'measure_unit': '%',
            'panc': {
                'low': None,
                'high': None,
            },
            'renal': {
                'low': 0.2,
                'high': 0.8,
            },
        },
    }

# calculate dry matter fat (%)


@st.cache_data
def calc_fat(fat, moisture):
    return (fat / (100-moisture)) * 100

# calculate dry matter protein (%)


@st.cache_data
def calc_protein(protein, moisture):
    return (protein / (100-moisture)) * 100

# calculate dry matter carbohydrate (%)


@st.cache_data
def calc_carbs(carbs, moisture):
    return (carbs / (100-moisture)) * 100

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


@st.cache_data
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


@st.cache_data
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


@st.cache_data
def display_charts(c, fat, fibre, protein, carbs, ash, phosphorus, chloride, sodium, sugar):
    st.subheader("Macronutrient Proportion Breakdown")
    if fat and fibre and protein:
        create_pie({c['fat']['desc']: fat,
                    c['protein']['desc']: protein,
                    c['carbs']['desc']: carbs,
                    c['fibre']['desc']: fibre,
                    c['ash']['desc']: ash})
    else:
        st.markdown("Insufficient data to display")
    st.divider()
    st.subheader("Macronutrient Percentages")
    if fat or fibre or protein:
        create_bar_chart({c['fat']['desc']: fat,
                          c['protein']['desc']: protein,
                          c['carbs']['desc']: carbs,
                          c['fibre']['desc']: fibre,
                          c['ash']['desc']: ash})
    else:
        st.markdown("Insufficient data to display")

    st.subheader("Micronutrient Percentages")

    if phosphorus or sodium or chloride:
        create_bar_chart({c['phosphorus']['desc']: phosphorus,
                          c['sodium']['desc']: sodium,
                          c['chloride']['desc']: chloride,
                          c['sugar']['desc']: sugar})
    else:
        st.markdown("Insufficient data to display")

# function to ensure metrics required for calculations have been submitted


@st.cache_data
def enforce_required(kcal_measure_weight, kcal, salt, salt_measure_weight, sugar, sugar_measure_weight):
    test_passed = True
    if not kcal_measure_weight or not kcal:
        st.warning(
            f":blue[Both calories and 'per *n* grams' needs to be provided.]")
        test_passed = False
    if salt and not salt_measure_weight:
        st.warning(
            ':blue[If salt is given, the *per grams* field needs to be provided.]')
        test_passed = False
    if sugar and not sugar_measure_weight:
        st.warning(
            ':blue[If sugar is given, the *per grams* field needs to be provided.]')
        test_passed = False
    return test_passed

# function to run pancreatitis tests


@st.cache_data
def run_panc_tests(c, dm_fat, dm_protein, dm_carbs, dm_sugar):
    result = []
    # test fat
    if dm_fat >= c['fat']['panc']['low'] and dm_fat <= c['fat']['panc']['high']:
        result.append({'nutrient': c['fat']['desc'],
                       'pass': True,
                       'reason': None})
    elif dm_fat < c['fat']['panc']['low']:
        result.append({'nutrient': c['fat']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': c['fat']['panc']['low'] - dm_fat,
                       'delta_pc': (((c['fat']['panc']['low'] - dm_fat) / dm_fat) * 100) if dm_fat else 100})
    elif dm_fat > c['fat']['panc']['high']:
        result.append({'nutrient': c['fat']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_fat - c['fat']['panc']['high'],
                       'delta_pc': (((dm_fat - c['fat']['panc']['high']) / c['fat']['panc']['high']) * 100)})
    #  test protein
    if dm_protein >= c['protein']['panc']['low'] and dm_protein <= c['protein']['panc']['high']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': True,
                       'reason': None})
    elif dm_protein < c['protein']['panc']['low']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': c['protein']['panc']['low'] - dm_protein,
                       'delta_pc': (((c['protein']['panc']['low'] - dm_protein) / dm_protein) * 100) if dm_protein else 100})
    elif dm_protein > c['protein']['panc']['high']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_protein - c['protein']['panc']['high'],
                       'delta_pc': (((dm_protein - c['protein']['panc']['high']) / c['protein']['panc']['high']) * 100)})
    #  test carbs
    if dm_carbs <= c['carbs']['panc']['high']:
        result.append({'nutrient': c['carbs']['desc'],
                       'pass': True,
                       'reason': None})
    else:
        result.append({'nutrient': c['carbs']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_carbs - c['carbs']['panc']['high'],
                       'delta_pc': (((dm_carbs - c['carbs']['panc']['high']) / c['carbs']['panc']['high']) * 100)})
    # test sugar
    if dm_sugar:
        result.append({'nutrient': c['sugar']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_sugar,
                       'delta_pc': 100})
    return result

# function to run renal tests


@st.cache_data
def run_renal_tests(c, dm_phosphorus, dm_protein, dm_sodium, dm_kcal_per_g):
    result = []
    # test phosphorus
    if dm_phosphorus >= c['phosphorus']['renal']['low'] and dm_phosphorus <= c['phosphorus']['renal']['high']:
        result.append({'nutrient': c['phosphorus']['desc'],
                       'pass': True, 'reason': None})
    elif dm_phosphorus < c['phosphorus']['renal']['low']:
        result.append({'nutrient': c['phosphorus']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': c['phosphorus']['renal']['low'] - dm_phosphorus,
                       'delta_pc': (((c['phosphorus']['renal']['low'] - dm_phosphorus) / dm_phosphorus) * 100) if dm_phosphorus else 100,
                       'unit': '%'})
    elif dm_phosphorus > c['phosphorus']['renal']['high']:
        result.append({'nutrient': c['phosphorus']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_phosphorus - c['phosphorus']['renal']['high'],
                       'delta_pc': (((dm_phosphorus - c['phosphorus']['renal']['high']) / c['phosphorus']['renal']['high']) * 100),
                       'unit': '%'})
    #  test protein
    if dm_protein >= c['protein']['renal']['low'] and dm_protein <= c['protein']['renal']['high']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': True,
                       'reason': None})
    elif dm_protein < c['protein']['renal']['low']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': False,
                       'reason': 'low',
                       'delta': c['protein']['renal']['low'] - dm_protein,
                       'delta_pc': (((c['protein']['renal']['low'] - dm_protein) / dm_protein) * 100) if dm_protein else 100,
                       'unit': '%'})
    elif dm_protein > c['protein']['renal']['high']:
        result.append({'nutrient': c['protein']['desc'],
                       'pass': False,
                       'reason': 'high',
                       'delta': dm_protein - c['protein']['renal']['high'],
                       'delta_pc': (((dm_protein - c['protein']['renal']['high']) / c['protein']['renal']['high']) * 100),
                       'unit': '%'})
    # test sodium
    dm_food_g_per_kcal = 1 / dm_kcal_per_g
    dm_sodium_g_per_kcal = dm_food_g_per_kcal * \
        (dm_sodium / 100) if dm_sodium else 0
    if dm_sodium_g_per_kcal >= c['sodium']['renal']['low'] and dm_sodium_g_per_kcal <= c['sodium']['renal']['high']:
        result.append(
            {'nutrient': c['sodium']['desc'],
                'pass': True,
                'reason': None})
    elif dm_sodium_g_per_kcal < c['sodium']['renal']['low']:
        result.append(
            {'nutrient': c['sodium']['desc'],
                'pass': False,
                'reason': 'low',
                'delta': c['sodium']['renal']['low'] - dm_sodium_g_per_kcal,
                'delta_pc': (((c['sodium']['renal']['low'] - dm_sodium_g_per_kcal) / dm_sodium_g_per_kcal) * 100) if dm_sodium_g_per_kcal else 100,
                'unit': 'g/kcal'})
    elif dm_sodium_g_per_kcal > c['sodium']['renal']['high']:
        result.append(
            {'nutrient': c['sodium']['desc'],
                'pass': False,
                'reason': 'high',
                'delta': dm_sodium_g_per_kcal - c['sodium']['renal']['high'],
                'delta_pc': (((dm_sodium_g_per_kcal - c['sodium']['renal']['low']) / c['sodium']['renal']['low']) * 100),
                'unit': 'g/kcal'})
    return result

#  function to display calculations


@st.cache_data
def display_calculations(c):
    dry_matter_stats_df = pd.DataFrame.from_dict([{
        c['fat']['desc']: st.session_state.dm_fat,
        c['protein']['desc']: st.session_state.dm_protein,
        c['carbs']['desc']: st.session_state.dm_carbs,
        c['fibre']['desc']: st.session_state.dm_fibre,
        c['ash']['desc']: st.session_state.dm_ash,
        c['phosphorus']['desc']: st.session_state.dm_phosphorus,
        c['sodium']['desc']: st.session_state.dm_sodium,
        c['chloride']['desc']: st.session_state.dm_chloride,
        c['sugar']['desc']: st.session_state.dm_sugar}])
    dry_matter_stats_df = pd.melt(dry_matter_stats_df,
                                  var_name='Dry Matter Constituent',
                                  value_name='Value (%)',
                                  ignore_index=True)
    dry_matter_stats_df.dropna(inplace=True)
    with st.container(border=True):
        st.markdown(f'Calories per dry matter gram (kcal): {
                    st.session_state.dm_kcal_per_g:.2f}')
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


@st.cache_data
def display_results(food_name, panc, renal):
    # pancreatitis diet
    with st.container(border=True):
        st.subheader('Pancreatitis Diet')
        if all(d.get('pass', False) == True for d in panc):
            st.success(
                f''':white[{food_name} is suitable for a pancreatitis diet]''', icon='👍')
        else:
            st.error(f''':white[{food_name} is not suitable for dogs with pancreatitis.]''',
                     icon='👎')
            for test in panc:
                if test['pass'] == False:
                    delta_pc = round(
                        test['delta_pc'], 2) if test['delta_pc'] <= 100 else 'over 100'
                    st.markdown(f"{test['nutrient']} is {delta_pc}% too {
                                test['reason']}")
    # renal diet
    with st.container(border=True):
        st.subheader('Renal diet')
        if all(d.get('pass', False) == True for d in renal):
            st.success(
                f''':white[{food_name} is suitable for a renal diet]''', icon='👍')
        else:
            st.error(f''':white[{food_name} is not suitable for dogs with kidney disease.]''',
                     icon='👎')
            for test in renal:
                if test['pass'] == False:
                    delta_pc = round(
                        test['delta_pc'], 2) if test['delta_pc'] <= 100 else 'over 100'
                    st.markdown(f"{test['nutrient']} is {delta_pc}% too {
                                test['reason']}")


""" PAGE 1 """
c = get_constituent_params()
st.title("Dog's Dinner Nutrient Calculator")
st.subheader(
    "'Dry Matter Basis' Calculation for Renal & Pancreatitis Diet Suitability")
st.warning(":blue[This app is currently in beta testing, therefore the results may be inaccurate. Please do not rely solely on the information provided here.]")
st.markdown("""The purpose of this calculator is to provide 'Dry Matter Basis' comparison between commercially available dog foods, where the 'analytical constituents' are provided by the manufacturer 'As Fed'.

Specifically, the calculator assesses the suitability of the dog food constituents for 'renal' and 'pancreatitis' diets, for dogs with kidney disease and/or disease of the pancreas.
            
The calculations used to establish the suitability of the dog food constituents submitted are based mainly on the information provided by the [All About Dog Food](https://allaboutdogfood.co.uk) website.
            """)

col_1, col_2, col_3 = st.columns(3, gap="medium")

with col_1:
    with st.container(border=True):
        st.header("Container Content ('As Fed')", divider="grey")

        st.session_state.food_name = st.text_input(
            label="Food name"
        )

        with st.container(border=True):
            cal_col_1, cal_col_2 = st.columns(2)
            with cal_col_1:
                kcal = st.number_input(
                    label="Calories (kcal)", key='kcal', min_value=0.00, max_value=100000.0
                )
            with cal_col_2:
                kcal_measure_weight = st.number_input(
                    label="Per Weight of Food (g)", key='kcal_measure_weight', min_value=0.00, max_value=100000.0
                )

        moisture = st.number_input(
            label="Moisture Content (%)", min_value=0.00, max_value=100.0
        )

        fat = st.number_input(
            label=f"Crude {c['fat']['desc']} ({c['fat']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        protein = st.number_input(
            label=f"Crude {c['protein']['desc']} ({c['protein']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        carbs = st.number_input(
            label=f"Crude {c['carbs']['desc']} ({c['carbs']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        fibre = st.number_input(
            label=f"Crude {c['fibre']['desc']} ({c['fibre']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        ash = st.number_input(
            label=f"{c['ash']['desc']} ({c['ash']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        phosphorus = st.number_input(
            label=f"{c['phosphorus']['desc']} ({c['phosphorus']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        sodium = st.number_input(
            label=f"{c['sodium']['desc']} ({c['sodium']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        chloride = st.number_input(
            label=f"{c['chloride']['desc']} ({c['chloride']['measure_unit']})", min_value=0.00, max_value=100.0
        )

        with st.container(border=True):
            salt_col_1, salt_col_2 = st.columns(2)
            with salt_col_1:
                salt = st.number_input(
                    label="Added Salt (g)", key='salt', min_value=0.00, max_value=100000.0
                )
            with salt_col_2:
                salt_measure_weight = st.number_input(
                    label="Per weight of food (g)", key="salt_measure_weight", min_value=0.00, max_value=100000.0
                )

        with st.container(border=True):
            sugar_col_1, sugar_col_2 = st.columns(2)
            with sugar_col_1:
                sugar = st.number_input(
                    label=f"{c['sugar']['desc']} ({c['sugar']['measure_unit']})", key='sugar', min_value=0.00, max_value=100000.0
                )
            with sugar_col_2:
                sugar_measure_weight = st.number_input(
                    label="Per weight of food (g)", key="sugar_measure_weight", min_value=0.00, max_value=100000.0
                )

        st.divider()
        st.caption(
            "Added salt is assumed to be composed of 40% Sodium and 60% Chloride, as referenced in the [European Union's Knowledge for Policy documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en)")

with col_2:
    with st.container(border=True):
        st.header("Dry Matter Basis (Results)", divider="grey")
        # run the calculations
        if enforce_required(kcal_measure_weight, kcal, salt, salt_measure_weight, sugar, sugar_measure_weight):
            st.session_state.dm_fat = round(
                calc_fat(fat, moisture), 3)
            st.session_state.dm_protein = round(
                calc_protein(protein, moisture), 3)
            st.session_state.dm_carbs = round(
                calc_carbs(carbs if carbs else 100 - (fat + protein + fibre + ash), moisture), 3)
            st.session_state.dm_fibre = round(
                calc_carbs(fibre, moisture), 3)
            st.session_state.dm_ash = round(
                calc_phosphorus(ash, moisture), 3)
            st.session_state.dm_phosphorus = round(
                calc_phosphorus(phosphorus, moisture), 3)
            st.session_state.dm_sodium = round(
                calc_sodium(sodium, salt, salt_measure_weight, moisture), 3)
            st.session_state.dm_chloride = round(
                calc_chloride(chloride, salt, salt_measure_weight, moisture), 3)
            st.session_state.dm_sugar = round(
                calc_sugar(sugar, sugar_measure_weight, moisture) if sugar and sugar_measure_weight else 0, 3)
            st.session_state.dm_kcal_per_g = round(
                calc_kcal_per_g(kcal, kcal_measure_weight, moisture), 3)
            st.session_state.dm_kcal_measure_weight = round(
                calc_kcal_measure_weight(kcal_measure_weight, moisture), 3)
            # display output
            display_calculations(c=c)
            st.divider()
            # display metrics in charts
            display_charts(c=c,
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
                    st.header("Diet Suitability", divider="grey")
                    # run tests & display results (provided calories have been entered; essential for calculations)
                    if st.session_state.dm_kcal_per_g:
                        st.session_state.panc = run_panc_tests(
                            c=c,
                            dm_fat=st.session_state.dm_fat,
                            dm_protein=st.session_state.dm_protein,
                            dm_carbs=st.session_state.dm_carbs,
                            dm_sugar=st.session_state.dm_sugar)

                        st.session_state.renal = run_renal_tests(
                            c=c,
                            dm_phosphorus=st.session_state.dm_phosphorus,
                            dm_protein=st.session_state.dm_protein,
                            dm_sodium=st.session_state.dm_sodium,
                            dm_kcal_per_g=st.session_state.dm_kcal_per_g)
                        # display results
                        display_results(food_name=st.session_state.food_name if st.session_state.food_name else "This food",
                                        panc=st.session_state.panc,
                                        renal=st.session_state.renal)
with st.container(border=True):
    st.header("Calculation Parameters")
    st.markdown(
        "The parameters for the calculations are currently set according to the information published at [All About Dog Food](https://www.allaboutdogfood.co.uk). However, these defaults (below) may be adjusted if required.")

with st.container(border=True):
    st.header("References")
    st.markdown("[All About Dog Food](https://www.allaboutdogfood.co.uk)")
    st.markdown("[European Union's Knowledge for Policy documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en)")
