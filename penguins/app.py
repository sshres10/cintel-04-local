# Import necessary libraries
import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from shiny import reactive
import palmerpenguins  # This package provides the Palmer Penguins dataset

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Set page options with a title and make the layout fillable
ui.page_opts(title="Penguin Data Shrestha", fillable=True)

# Create a sidebar that is open by default
with ui.sidebar(open="open"):
    ui.h2("Sidebar_Shrestha")  # Add a second-level header to the sidebar
    ui.input_selectize(
        "selected_attribute",  # Name of the input
        "Choose a column:",  # Label for the dropdown
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        selected="bill_length_mm", 
    )
    ui.input_numeric(
        "plotly_bin_count",  # Name of the input
        "Histogram Bin Count(Plotly Scatterplot: Species",  # Label for the numeric input
        value=10,  # Adding a default value for clarity
    )
    ui.input_slider(
        "seaborn_bin_count",  # Name of the input
        "Number of bins for Seaborn histogram",  # Label for the slider
        min=1,  # Minimum value for the slider
        max=50,  # Maximum value for the slider
        value=10,  # Default value for the slider
    )
    ui.input_checkbox_group(
        "selected_species",  # Name of the input
        "Filter by species:",  # Label for the checkbox group
        choices=["Adelie", "Gentoo", "Chinstrap"],  # Checkbox options
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selected options
        inline=False,  # Display the checkboxes inline or stacked (True/False)
    )
    ui.hr()  # Text for the hyperlink
    ui.a(
        "GitHub", href="https://github.com/sshres10/cintel-03-reactive", target="_blank"
    )  # Open the link in a new tab

# Define a consistent color scheme for plots
color_discrete_map = {
    "Adelie": "#1f77b4",  # blue
    "Gentoo": "#ff7f0e",  # orange
    "Chinstrap": "#2ca02c",  # green
}
with ui.layout_columns():  # Define the main layout of the page with two columns
    # Histogram Plot 1
    @render_plotly
    def plot1():
        df = filtered_data()
        attr = input.selected_attribute() or "bill_length_mm"
        fig = px.histogram(
            df,
            x=attr,
            nbins=input.plotly_bin_count(),
            title=f"Distribution of {attr.replace('_', ' ')}",
            labels={attr: attr.replace("_", " ").title()},
            color_discrete_map=color_discrete_map,
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        return fig

    # Histogram Plot 2
    @render_plotly
    def plot2():
        df = filtered_data()
        attr = input.selected_attribute() or "flipper_length_mm"
        fig = px.histogram(
            df,
            x=attr,
            nbins=input.plotly_bin_count(),
            title=f"Distribution of {attr.replace('_', ' ')}",
            labels={attr: attr.replace("_", " ").title()},
            color_discrete_map=color_discrete_map,
        )
        fig.update_layout(template="plotly_white", showlegend=False)
        return fig

    # Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            df = filtered_data()
            fig = px.scatter(
                df,
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
                title="Scatterplot by Species",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "bill_depth_mm": "Bill Depth (mm)",
                },
                color_discrete_map=color_discrete_map,
            )
            fig.update_layout(template="plotly_white")
            return fig

    # DataTable
    @render.data_frame
    def render_penguins_df():
        return filtered_data()

    # Data Grid
    @render.data_frame
    def render_penguins_data_grid():
        return filtered_data()


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.


@reactive.calc
def filtered_data():
    selected_species = input.selected_species()
    selected_attribute = input.selected_attribute()

# Filter the DataFrame based on the selected species
    filtered_df = penguins_df[penguins_df["species"].isin(selected_species)]

# Additionally, if the selected attribute is not None and drop NA values for that column
    if selected_attribute:
        filtered_df = filtered_df.dropna(subset=[selected_attribute])

    return filtered_df
