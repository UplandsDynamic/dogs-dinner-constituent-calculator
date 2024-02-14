import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")

# set variables in session state
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
if "dm_ash" not in st.session_state:
    st.session_state.dm_ash = 0
if "dm_salt" not in st.session_state:
    st.session_state.dm_salt = 0
if "dm_sugar" not in st.session_state:
    st.session_state.dm_sugar = 0
if "dm_kcal_per_g" not in st.session_state:
    st.session_state.dm_kcal_per_g = 0
if "dm_weight_in_g" not in st.session_state:
    st.session_state.dm_weight_in_g = 0

st.title("Dog's Dinner Nutrient Calculator")
st.subheader(
    "'Dry Matter Basis' Calculation for Renal & Pancreatitis Diet Suitability")

col_1, col_2, col_3 = st.columns(3, gap="medium")

with col_1:
    with st.container(border=True):
        st.header("Container Content ('As Fed')", divider="grey")

        st.session_state.food_name = st.text_input(
            label="Food name"
        )

        full_container_weight = st.number_input(
            label="Full container weight (g)", min_value=1, max_value=100000
        )

        kcal_per_g = st.number_input(
            label="Kcal per gram", min_value=0.00, max_value=100000.0
        )

        moisture = st.number_input(
            label="Moisture content (%)", min_value=0.00, max_value=100.0
        )

        fat = st.number_input(
            label="Crude Fat (%)", min_value=0.00, max_value=100.0
        )

        protein = st.number_input(
            label="Crude Protein (%)", min_value=0.00, max_value=100.0
        )

        carbs = st.number_input(
            label="Crude Carbohydrate (%)", min_value=0.00, max_value=100.0
        )

        fibre = st.number_input(
            label="Crude Fibre (%)", min_value=0.00, max_value=100.0
        )

        ash = st.number_input(
            label="Crude Ash (%)", min_value=0.00, max_value=100.0
        )

        phosphorus = st.number_input(
            label="Phosphorus (%)", min_value=0.00, max_value=100.0
        )

        sodium = st.number_input(
            label="Sodium (%)", min_value=0.00, max_value=100.0
        )

        chloride = st.number_input(
            label="Chloride (%)", min_value=0.00, max_value=100.0
        )

        salt = st.number_input(
            label="Added salt (g)", min_value=0.00, max_value=10000.0
        )

        sugar = st.number_input(
            label="Added sugars (g)", min_value=0.00, max_value=10000.0
        )

        st.divider()
        st.caption(
            "Added salt is assumed to be composed of 40% Sodium and 60% Chloride, as referenced in the [European Union's Knowledge for Policy documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en)")

with col_2:
    with st.container(border=True):
        st.header("Dry Matter Basis (Results)", divider="grey")

        # calculate fat
        @st.cache_data
        def calc_fat(fat, moisture):
            return (fat / (100-moisture)) * 100

        # calculate protein
        @st.cache_data
        def calc_protein(protein, moisture):
            return (protein / (100-moisture)) * 100

        # calculate carbohydrate
        @st.cache_data
        def calc_carbs(carbs, moisture):
            return (carbs / (100-moisture)) * 100

        # calculate fibre
        @st.cache_data
        def calc_fibre(fibre, moisture):
            return (fibre / (100-moisture)) * 100

        # calculate ash
        @st.cache_data
        def calc_ash(ash, moisture):
            return (ash / (100-moisture)) * 100

        # calculate phosphorus
        @st.cache_data
        def calc_phosphorus(phosphorus, moisture):
            return (phosphorus / (100-moisture)) * 100

        # calculate sodium
        @st.cache_data
        def calc_sodium(sodium, salt, moisture):
            return ((sodium + ((salt * 0.4) / full_container_weight * 100)) / (100-moisture)) * 100

        # calculate chloride
        @st.cache_data
        def calc_chloride(chloride, salt, moisture):
            return ((chloride + ((salt * 0.6) / full_container_weight * 100)) / (100-moisture)) * 100

        # calculate sugar
        @st.cache_data
        def calc_sugar(sugar, full_container_weight, moisture):
            return ((sugar / full_container_weight * 100) / (100-moisture)) * 100

        # calculate dry matter weight
        @st.cache_data
        def calc_weight_g(full_container_weight, moisture):
            return (full_container_weight * (100-moisture)) / 100

        # calculate kcal/g
        @st.cache_data
        def calc_kcal_per_g(kcal_per_g, moisture):
            return ((moisture / 100) * kcal_per_g) + kcal_per_g

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
        def display_charts(fat, fibre, protein, carbs, ash, phosphorus, chloride, sodium, sugar):
            st.subheader("Macronutrient Proportion Breakdown")
            if fat and fibre and protein:
                create_pie({'Crude Fat': fat, 'Crude Protein': protein,
                            'Crude Carbohydrates': carbs, 'Crude Fibre': fibre, 'Crude Ash': ash})
            else:
                st.markdown("Insufficient data to display")
            st.divider()
            st.subheader("Macronutrient Percentages")
            if fat or fibre or protein:
                create_bar_chart({'Crude Fat': fat, 'Crude Protein': protein,
                                  'Crude Carbohydrates': carbs, 'Crude Fibre': fibre, 'Crude Ash': ash})
            else:
                st.markdown("Insufficient data to display")

            st.subheader("Micronutrient Percentages")

            if phosphorus or sodium or chloride:
                create_bar_chart({'Phosphorus': phosphorus, 'Sodium': sodium,
                                  'Chloride': chloride, 'Added Sugars': sugar})
            else:
                st.markdown("Insufficient data to display")

        # run the calculations
        if full_container_weight:
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
                calc_sodium(sodium, salt, moisture), 3)
            st.session_state.dm_chloride = round(
                calc_chloride(chloride, salt, moisture), 3)
            st.session_state.dm_sugar = round(
                calc_sugar(sugar, full_container_weight, moisture), 3)
            st.session_state.dm_kcal_per_g = round(
                calc_kcal_per_g(kcal_per_g, moisture), 3)
            st.session_state.dm_weight_in_g = round(
                calc_weight_g(full_container_weight, moisture), 3)

            # write output
            st.write(f"Dry Matter Weight In Grams: {
                st.session_state.dm_weight_in_g:.2f}")
            st.write(f"Dry Matter Kcal Per Gram: {
                st.session_state.dm_kcal_per_g:.2f}")
            st.write(f"Dry Matter Fat Content: {
                st.session_state.dm_fat:.2f}%")
            st.write(f"Dry Matter Protein Content: {
                st.session_state.dm_protein:.2f}%")
            st.write(f"Dry Matter Carbohydrate Content: {
                st.session_state.dm_carbs:.2f}%")
            st.write(f"Dry Matter Fibre Content: {
                st.session_state.dm_fibre:.2f}%")
            st.write(f"Dry Matter Ash Content: {
                st.session_state.dm_ash:.2f}%")
            st.write(f"Dry Matter Phosphorus Content: {
                st.session_state.dm_phosphorus:.2f}%")
            st.write(f"Dry Matter Sodium Content: {
                st.session_state.dm_sodium:.2f}%")
            st.write(f"Dry Matter Chloride Content: {
                st.session_state.dm_chloride:.2f}%")
            st.write(f"Dry Matter Added Sugars Content: {
                st.session_state.dm_sugar:.2f}%")

        st.divider()

        # display metrics in charts
        display_charts(ash=st.session_state.dm_ash,
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

        # function to run pancreatitis tests
        @st.cache_data
        def run_panc_tests(dm_fat, dm_protein, dm_carbs, dm_sugar):
            result = []
            # test fat
            if dm_fat >= 5 and dm_fat <= 10:
                result.append({'nutrient': 'Crude Fat',
                              'pass': True, 'reason': None})
            elif dm_fat < 5:
                result.append({'nutrient': 'Crude Fat',
                              'pass': False, 'reason': 'low'})
            elif dm_fat > 10:
                result.append({'nutrient': 'Crude Fat',
                              'pass': False, 'reason': 'high'})
            #  test protein
            if dm_protein >= 20 and dm_protein <= 30:
                result.append({'nutrient': 'Crude Protein',
                              'pass': True, 'reason': None})
            elif dm_protein < 20:
                result.append({'nutrient': 'Crude Protein',
                              'pass': False, 'reason': 'low'})
            elif dm_protein > 30:
                result.append({'nutrient': 'Crude Protein',
                              'pass': False, 'reason': 'high'})
            #  test carbs
            if dm_carbs <= 60:
                result.append({'nutrient': 'Crude Carbohydrate',
                              'pass': True, 'reason': None})
            else:
                result.append({'nutrient': 'Crude Carbohydrate',
                              'pass': False, 'reason': 'high'})
            # test sugar
            if dm_sugar:
                result.append({'nutrient': 'Crude Sugar',
                              'pass': False, 'reason': 'high'})
            return result

        # function to run renal tests
        @st.cache_data
        def run_renal_tests(dm_phosphorus, dm_protein, dm_sodium, dm_kcal_per_g, dm_weight_in_g):
            result = []
            # test phosphorus
            if dm_phosphorus >= 0.2 and dm_phosphorus <= 0.8:
                result.append({'nutrient': 'Phosphorus',
                              'pass': True, 'reason': None})
            elif dm_phosphorus < 0.2:
                result.append({'nutrient': 'Phosphorus',
                               'pass': False, 'reason': 'low'})
            elif dm_phosphorus > 0.8:
                result.append({'nutrient': 'Phosphorus',
                               'pass': False, 'reason': 'high'})
            #  test protein
            if dm_protein >= 15 and dm_protein <= 30:
                result.append({'nutrient': 'Crude Protein',
                               'pass': True, 'reason': None})
            elif dm_protein < 15:
                result.append({'nutrient': 'Protein',
                               'pass': False, 'reason': 'low'})
            elif dm_protein > 30:
                result.append({'nutrient': 'Protein',
                               'pass': False, 'reason': 'high'})

            dm_sodium = dm_sodium
            total_calories = 3898
            calories_per_n_grams = 3.90
            calorie_calc_grams = 1000
            min_sodium_per_g = 0.0004
            max_sodium_per_g = 0.0012

            st.write(f'Actual sodium % = {dm_sodium}')
            # calculation where total calories given
            st.write(f'Min target sodium % = {
                     min_sodium_per_g * total_calories}')
            st.write(f'Max target sodium % = {
                     max_sodium_per_g * total_calories}')
            # calculation where calories per n grams given
            st.write(f'Max target sodium % = {
                     min_sodium_per_g / calorie_calc_grams * calories_per_n_grams}')
            st.write(f'Max target sodium % = {
                     max_sodium_per_g / calorie_calc_grams * calories_per_n_grams}')

            # test sodium
            if (dm_weight_in_g * (dm_sodium / 100)) >= 0.0004 * (dm_kcal_per_g * dm_weight_in_g) and (dm_weight_in_g * (dm_sodium / 100)) <= 0.0012 * (dm_kcal_per_g * dm_weight_in_g):
                result.append(
                    {'nutrient': 'Sodium', 'pass': True, 'reason': None})
            elif (dm_weight_in_g * (dm_sodium / 100)) < 0.0004 * (dm_kcal_per_g * dm_weight_in_g):
                result.append(
                    {'nutrient': 'Sodium', 'pass': False, 'reason': 'low'})
            elif (dm_weight_in_g * (dm_sodium / 100)) > 0.0012 * (dm_kcal_per_g * dm_weight_in_g):
                result.append(
                    {'nutrient': 'Sodium', 'pass': False, 'reason': 'high'})
            return result

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
                            st.markdown(f"{test['nutrient']} is {
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
                            st.markdown(f"{test['nutrient']} is {
                                        test['reason']}")

        # run tests
        st.session_state.panc = run_panc_tests(dm_fat=st.session_state.dm_fat, dm_protein=st.session_state.dm_protein,
                                               dm_carbs=st.session_state.dm_carbs, dm_sugar=st.session_state.dm_sugar)

        st.session_state.renal = run_renal_tests(dm_phosphorus=st.session_state.dm_phosphorus, dm_protein=st.session_state.dm_protein,
                                                 dm_sodium=st.session_state.dm_sodium, dm_kcal_per_g=st.session_state.dm_kcal_per_g, dm_weight_in_g=st.session_state.dm_weight_in_g)

        # display results
        display_results(food_name=st.session_state.food_name if st.session_state.food_name else "This food",
                        panc=st.session_state.panc,
                        renal=st.session_state.renal)


with st.container(border=True):
    st.header("References")
    st.markdown("[European Union's Knowledge for Policy documentation](https://knowledge4policy.ec.europa.eu/health-promotion-knowledge-gateway/dietary-saltsodium_en)")
