"""
Streamlit app for collecting orders from Mister TAMO's menu

This app presents the full Mister TAMO menu as captured from the official
Google Sites menu (December 2025) and allows multiple users to select items
and quantities.  At the bottom of the page the app displays an itemised
summary and the total cost of the order.  Prices are expressed in euros and
reflect table‑service pricing as shown on the menu.  If you wish to run
the app locally you need to have Python 3.7+ and the streamlit package
installed (`pip install streamlit`).  Then run it using:

  streamlit run ordering_app.py

Share the resulting URL with your friends so they can add their orders.
"""

import streamlit as st
from collections import defaultdict


def build_menu() -> dict:
    """Return the Mister TAMO menu as a dictionary.

    The structure is a mapping from category name to a list of tuples
    containing (item_name, price).  Prices are floats representing euros.
    """
    menu = {
        "Aperitivo": [
            ("Formula Gajardo (Apericena)", 15.0),
            ("Formula Norcino (Apericena)", 15.0),
            ("Formula Aperitamo (Aperitivo)", 12.0),
        ],
        "Analcolici (non‑alcoholic)": [
            ("Tamo Fruit (Mela, Arancia, Anguria)", 5.0),
            ("Hawaii (Fragola, Ananas)", 5.0),
            ("Esotic (Passion Fruit, Lime, Zucchero di canna, Ginger Beer)", 5.0),
            ("Virgin Mojito (Tonica, Lime, Zucchero di canna, Menta)", 5.0),
            ("Virgin Colada (Ananas, Cocco)", 5.0),
            ("Charlie Tample (Ginger Ale, Cranberry Juice)", 5.0),
        ],
        "Spritz": [
            ("Apertas (Aperol, Cedrata)", 6.0),
            ("Aperol Spritz", 6.0),
            ("Campari Spritz", 6.0),
            ("Calabro Spritz (Amaro del Capo Red Hot, Prosecco)", 7.0),
            ("Hugo (Liquore di Sambuco, Prosecco, Menta)", 6.0),
            ("Martini Royale (Martini Bianco, Lime, Prosecco)", 6.0),
            ("Melon Spritz (Midori, Prosecco)", 6.0),
            ("Passoa Spritz (Passoa, Prosecco)", 6.0),
            ("Violetta Spritz (Liquore alla Violetta, Prosecco)", 6.0),
        ],
        "Negroni": [
            ("Negroni", 8.0),
            ("Negroni Sbagliato", 8.0),
            ("Boulevardier", 8.0),
            ("Negroni Bianco", 8.0),
            ("Negroni al Cioccolato", 8.0),
            ("Americano", 8.0),  # appears on the after‑dinner drinks list
        ],
        "Gin Tonic": [
            ("Gin Tonic", 8.0),
            ("Gin Lemon", 8.0),
            ("Tanqueray Tonic", 10.0),
            ("Tanqueray No. Ten Tonic", 12.0),
            ("Malfy Pink Tonic", 12.0),
            ("Bombay Tonic", 12.0),
            ("Gin Mare Tonic", 12.0),
        ],
        "Mule": [
            ("Moscow Mule", 8.0),
            ("London Mule", 8.0),
            ("Mexican Mule", 8.0),
            ("Suffering Busterd", 8.0),
        ],
        "Pestati": [
            ("Mojito", 9.0),
            ("Caipiroska", 9.0),
            ("Caipiroska Fragola", 9.0),
            ("Caipiroska Frutti Rossi", 9.0),
            ("Caipiroska Passion Fruit", 9.0),
        ],
        "Sour": [
            ("Whiskey Sour", 8.0),
            ("Midori Sour", 8.0),
            ("Di Saronno Sour", 8.0),
            ("New York Sour", 8.0),
        ],
        "Cocktail Pre‑Dinner": [
            ("Morgana", 8.0),
            ("Sky Walker", 8.0),
            ("Paloma", 8.0),
            ("Tequila Sunrise", 8.0),
        ],
        "Cocktail After‑Dinner": [
            ("Mister Tamo", 8.0),
            ("Alexander", 8.0),
            ("Satan’s Whiskers", 8.0),
            ("Long Island Ice Tea", 8.0),
            ("Japanese Ice Tea", 8.0),
            ("Miami Ice Tea", 8.0),
            ("Pina Colada", 8.0),
        ],
        "Tiki Cocktails": [
            ("Jungle Birth", 10.0),
            ("Mister Funk", 10.0),
        ],
        "Salty dishes (Brunch)": [
            ("Avocado Toast", 10.0),
            ("Eggs Royal", 12.0),
            ("Club Sandwich Tacchino", 9.0),
            ("Club Sandwich Royal", 9.0),
            ("English Breakfast", 10.0),
            ("American Breakfast", 12.0),
            ("French Toast", 9.0),
            ("Caesar Salad (Brunch)", 12.0),
        ],
        "Primi e Secondi (Brunch)": [
            ("Tonnarello Cacio e Pepe", 11.0),
            ("Tonnarello Carbonara", 11.0),
            ("Mezza Manica all’Amatriciana", 11.0),
            ("Tonnarello Pomodoro e Basilico", 9.0),
            ("Tagliata di Petto di Pollo (Lime e Menta)", 13.0),
            ("Veggy Wrap", 9.0),
        ],
        "Sweet brunch (Pancakes e Waffles)": [
            ("Baby Pancakes", 5.0),
            ("Pancakes Cioccolato Bianco e Frutti di Bosco", 8.0),
            ("Pancakes Nutella e Banana", 7.0),
            ("Pancakes Nutella, Fragole e Panna", 8.0),
            ("Pancakes Pistacchio", 7.0),
            ("Pancakes Sciroppo Acero", 8.0),
            ("Waffle Crema e Frutti di Bosco", 8.0),
            ("Waffle Nutella e Fragola", 7.0),
            ("Waffle Pistacchio", 7.0),
            ("Waffle Sciroppo Acero", 7.0),
            ("Waffle Cioccolato Bianco e Frutti di Bosco", 8.0),
        ],
        "Bio Zone": [
            ("Centrifugato Depurante", 7.0),
            ("Centrifugato Antiossidante", 7.0),
            ("Centrifugato Digestiva", 7.0),
            ("Centrifugato Tonificante", 7.0),
            ("Centrifugato Rinfrescante", 7.0),
            ("Frullato fai da te", 6.0),
            ("Spremuta di Arance", 3.5),
            ("Spremuta di Pompelmo", 4.0),
        ],
        "Caffetteria": [
            ("Caffè Espresso", 2.0),
            ("Caffè Corretto", 2.5),
            ("Caffè Americano", 2.0),
            ("Caffè Shekerato", 3.0),
            ("Caffè e Latte", 1.8),
            ("Cappuccino", 2.0),
            ("Cappuccino Soya/Avena/Senza Lattosio", 2.5),
            ("Latte Macchiato", 1.8),
            ("Ginseng Piccolo", 2.0),
            ("Ginseng Grande", 2.5),
            ("Orzo Piccolo", 2.0),
            ("Orzo Grande", 2.5),
            ("Marocchino", 2.5),
        ],
        "Caffè Special": [
            ("Mister Tamo (espresso, Nutella, crema di latte, pistacchio)", 3.5),
            ("Pistacchioso", 3.0),
            ("Caramelloso", 3.0),
            ("Nocciolino", 3.0),
            ("Coccoloso", 3.0),
            ("Pannoso", 3.0),
            ("Marocchino Special", 3.0),
            ("Shekerato Special", 3.5),
        ],
        "Cioccolate Calde": [
            ("Cioccolata Calda al Latte", 3.5),
            ("Cioccolata Calda Fondente", 3.5),
            ("Cioccolata Calda con Panna", 4.0),
            ("Cioccolata Calda con Panna e Fragole", 5.0),
        ],
        "Dolci – monoporzioni e torte": [
            ("Tortino dal Cuore Caldo", 7.0),
            ("Monoporzione Cioccolampone", 6.0),
            ("Monoporzione Gianduiotto", 6.0),
            ("Caprese Croccante", 6.0),
            ("Tiramisù 2.0 Cioccolato e Caffè", 6.0),
            ("Monoporzione Nuvola", 6.0),
            ("Monoporzione Meringata", 6.0),
            ("Monoporzione Ambra", 6.0),
            ("Cheesecake Nutella (monoporzione)", 6.0),
            ("Cheesecake Frutti Rossi (monoporzione)", 6.0),
            ("Cheesecake Pistacchio (monoporzione)", 6.0),
            ("Cheesecake Caramello Salato (monoporzione)", 6.0),
            ("Eclair Cioccolato", 3.5),
            ("Torta Sacher artigianale", 5.0),
            ("Tiramisù Gluten/Lacto Free", 7.0),
            ("Tortina Vegan di Carote", 4.0),
            ("Brownies (anche gluten free)", 4.0),
            ("Muffin Gluten Free", 3.5),
            ("Torta della Nonna classica", 3.5),
            ("Crostata Marmellata artigianale", 3.5),
            ("Crostata Vegan – Albicocca e Avena", 3.5),
        ],
        "Dolci – pancakes": [
            ("Pancakes Bueno", 9.0),
            ("Pancakes Nutella e Banana", 7.0),
            ("Pancakes Cioccolato Bianco e Frutti Rossi", 8.0),
            ("Pancakes Sciroppo Acero", 8.0),
            ("Pancakes Nutella, Fragole e Panna", 8.0),
            ("Pancakes Pistacchio", 8.0),
        ],
        "Dolci – waffle": [
            ("Waffle Sciroppo Acero, Banana e muesli", 7.0),
            ("Waffle Nutella e Fragola", 8.0),
            ("Waffle Crema e Frutti Rossi", 8.0),
            ("Waffle Pistacchio", 8.0),
            ("Waffle Cioccolato Bianco e Frutti Rossi", 8.0),
        ],
        "Dolci – muffin, donuts, biscotti": [
            ("Muffin Vaniglia", 2.5),
            ("Muffin Albicocca", 2.5),
            ("Muffin Cioccolato", 2.5),
            ("Muffin Mirtillo", 2.5),
            ("Muffin Pistacchio", 2.5),
            ("Muffin Cioccolato Bianco", 2.5),
            ("Muffin Nutella Ferrero", 3.0),
            ("Muffin Oreo", 3.0),
            ("Donut Oreo", 2.5),
            ("Donut Cioccolato", 2.5),
            ("Donut Marshmallow", 2.5),
            ("Macaron (vari gusti)", 2.5),
            ("Pasticceria mignon (per pezzo)", 1.5),
            ("Mix Pasticceria mignon (5 pezzi)", 6.0),
            ("Pasticciotto Pugliese (crema o amarena)", 2.0),
            ("Cornetto Gluten Free", 2.7),
            ("Lieviti assortiti", 1.5),
            ("Biscotteria da the (per pezzo)", 0.8),
            ("Mix Biscotteria da the (5 pezzi)", 3.5),
            ("Biscotti Zenzero e Cannella", 1.0),
            ("Biscotti Mirtillo e Bacche di Goji", 1.0),
        ],
        "Vini – bianchi": [
            ("Calice Gewürztraminer", 6.0),
            ("Calice Kikè (Cantina Fina)", 6.0),
            ("Calice Ribolla Gialla", 5.5),
            ("Calice Sauvignon", 5.5),
            ("Calice Chardonnay", 5.5),
        ],
        "Vini – rossi": [
            ("Calice Shiraz", 6.0),
            ("Calice Primitivo", 5.5),
            ("Calice Chianti Classico", 5.5),
        ],
        "Bollicine (Prosecco)": [
            ("Calice Prosecco Cuvée", 5.0),
        ],
        "Birre (bottiglia 33 cl)": [
            ("Tennent’s", 4.0),
            ("Beck’s", 4.0),
            ("Menabrea", 4.0),
            ("Menabrea Rossa", 4.0),
            ("Messina Cristalli di Sale", 4.0),
            ("Ichnusa", 4.0),
            ("Ichnusa Non Filtrata", 4.0),
        ],
        "Soft drinks": [
            ("Coca‑cola (bottiglia vetro)", 3.5),
            ("Coca‑cola Zero (bottiglia vetro)", 3.5),
            ("Fanta (bottiglia vetro)", 3.5),
            ("Aranciata amara", 2.5),
            ("Schweppes Ginger Beer", 3.5),
            ("Schweppes Lemon", 3.5),
            ("Schweppes Soda", 3.5),
            ("Red Bull", 3.5),
            ("Chinotto (bottiglia vetro)", 3.5),
            ("Cedrata", 3.5),
            ("Thè freddo (PET)", 3.0),
            ("Thè freddo (bicchiere)", 2.5),
            ("Succo di frutta (vari gusti)", 3.0),
            ("Succo mirtillo", 3.5),
            ("Succo pesca e mango", 3.5),
            ("Succo melograno", 3.5),
        ],
        "Rum (selezione)": [
            ("Havana 7", 6.0),
            ("Legendario Elixir", 8.0),
            ("Barcelò", 8.0),
            ("Don Papa", 8.0),
            ("Zacapa 23", 9.0),
        ],
        "Amari e Grappe": [
            ("Jägermeister", 3.5),
            ("Lucano", 3.5),
            ("Montenegro", 3.5),
            ("Amaro del Capo", 3.5),
            ("Amaro del Capo Red Hot", 4.5),
            ("Brancamenta", 3.5),
            ("Fernet Branca", 3.5),
            ("Averna", 3.5),
            ("Unicum", 3.5),
            ("Grappa 3.0", 3.5),
            ("Grappa 3.0 barricata", 4.6),
            ("Grappa 903 barricata", 4.6),
        ],
        "Whisky & Cognac": [
            ("Jack Daniel’s", 5.8),
            ("Jim Beam", 5.8),
            ("Wild Turkey", 5.8),
            ("Cognac Hartell VS", 5.5),
        ],
        "Spirits": [
            ("Bitter Campari", 4.5),
            ("Stravecchio", 3.5),
            ("Vecchia Romagna", 3.5),
            ("Disaronno", 3.5),
            ("Elisir Gambrinus", 3.5),
            ("Limoncello", 3.5),
            ("Sambuca Molinari", 3.5),
        ],
        "Tea & Infusions": [
            ("English Breakfast (Black Tea)", 3.5),
            ("Earl Grey (Black Tea)", 3.5),
            ("Earl Grey Night (decaffeinated)", 3.5),
            ("Lemon (Black Tea)", 3.5),
            ("Winter Tea (Black Tea con Cannella e Chiodi di Garofano)", 3.5),
            ("Red Fruits (Black Tea con frutti rossi)", 3.5),
            ("China Green Tea", 3.5),
            ("Wood Flavour (Fruit Infusion)", 3.5),
            ("Blueberry Cherry (Fruit Infusion)", 3.5),
            ("Moonlight (Herbal Infusion al Finocchio)", 3.5),
            ("Golden Flowers (Herbal Infusion)", 3.5),
        ],
    }
    return menu


def main() -> None:
    st.set_page_config(page_title="Mister TAMO Order Manager", page_icon="🍽️")
    st.title("Mister TAMO – gestore ordini per la colazione/brunch/aperitivo")
    st.write(
        "Seleziona le quantità per ogni prodotto desiderato. I prezzi sono in euro e"
        " comprendono il servizio al tavolo. Al termine della selezione troverai un"
        " riassunto dell'ordine con il totale."
    )

    menu = build_menu()
    # Use a defaultdict to collect item quantities across categories
    order_quantities: dict[str, int] = defaultdict(int)

    # Iterate over categories, displaying each inside an expander for clarity
    for category, items in menu.items():
        with st.expander(category, expanded=False):
            st.write(f"**{category}**")
            for item_name, price in items:
                key = f"qty_{category}_{item_name}"
                qty = st.number_input(
                    label=f"{item_name} – {price:.2f} €", min_value=0, step=1, key=key
                )
                if qty:
                    order_quantities[(item_name, price)] += int(qty)

    # Compute summary
    st.header("Riepilogo ordine")
    if order_quantities:
        total = 0.0
        summary_lines = []
        for (item_name, price), qty in order_quantities.items():
            line_total = price * qty
            total += line_total
            summary_lines.append(
                f"{item_name} × {qty} → {line_total:.2f} €"
            )
        st.markdown("\n".join(summary_lines))
        st.markdown(f"**Totale:** {total:.2f} €")
    else:
        st.info("Nessun prodotto selezionato. Usa i menu per aggiungere articoli al tuo ordine.")


if __name__ == "__main__":
    main()