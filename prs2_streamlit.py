'''
Autore: Stefano Sambo
Ultimo aggiornamento: 04/01/25
Descrizione: Applicazione streamlit di prova'''

import streamlit as st
import prs2_grafici as gr
import prs2_varie as v
import prs2_dataset as ds
import altair as alt
import polars as pl






if "page" not in st.session_state:
    st.session_state.page = "Home" #prima schermata=home

def page_change(page): #per semplificare i cambi di schermata
    st.session_state.page = page 

def return_home_button(): #tasto per tornare alla pagina home
    st.button("Torna alla Homepage", on_click=lambda: page_change("Home"))

def single_game_graph_show(player_name): #sfrutta la funzione di prs2_grafici per mostrare tutti i grafici di tutte le partite
    games=ds.player_gamelogs_df(player_name)
    for _, game in games.iterrows():
        game_id = game["Game_ID"]
        game_events = ds.player_modifiedevents_list(game_id, player_name)
        if len(game_events) > 0:
            st.altair_chart(gr.singlegame_fg_graph(game_events))

menu = st.sidebar.selectbox(
    "Pagine",
    ["Home", "Introduzione", "Percentuali Condizionate", "Statistiche Generali", "Statistiche Top 5"],
    index=["Home", "Introduzione", "Percentuali Condizionate", "Statistiche Generali", "Statistiche Top 5"].index(st.session_state.page)
)



page_change(menu)

if st.session_state.page == "Home":
    st.markdown("<h1 style='text-align: center;'> NBA: ANALISI STATISTICHE E SEQUENZE DI TIRO </h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.nbareligion.com/wp-content/uploads/2020/01/logo-nba.jpg" width="400">
    </div>
    """,
    unsafe_allow_html=True
)
    st.divider()
    st.markdown("### Benvenuto! Scegli una pagina per iniziare")

    st.button("Non capisci qualcosa? Premi qua", on_click=lambda: page_change("Introduzione"))
    st.button("Vai alle percentuali condizionate", on_click=lambda: page_change("Percentuali Condizionate"))
    st.button("Vai alle statistiche generali", on_click=lambda: page_change("Statistiche Generali"))
    st.button("Statistiche 5 migliori giocatori", on_click=lambda: page_change("Statistiche Top 5"))

elif st.session_state.page == "Introduzione":
    st.markdown("<h1 style='text-align: center;'> Introduzione</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Premesse
La National Basketball Association, meglio nota come **NBA**, è la prima lega statunitense di pallacanestro, dove tutti i migliori giocatori del mondo competono per tutta la stagione con l'obiettivo di vincere l'anello.
Sebbene il livello sia il più alto possibile, ogni giocatore di ogni campionato esistente, partendo appunto dall'NBA fino ai campionati amatoriali, conosce il concetto di **mano calda e mano fredda**:
- Se hai appena fatto una serie consecutiva di canestri è più probabile che anche il tiro successivo entri;
- Viceversa, venendo da più errori di fila, la probabilità di segnare è più bassa.
        """)


    with col2:
        st.image("https://cdn.vox-cdn.com/thumbor/TFJlC8wjt3UT_r2F-U0oEEIuUqU=/0x0:4081x2721/1400x1400/filters:focal(1823x499:2475x1151):format(jpeg)/cdn.vox-cdn.com/uploads/chorus_image/image/55431127/usa_today_10003570.0.jpg",
                 caption="Kyle Korver, uno dei giocatori migliori della storia nella percentuale da 3pt")

    st.markdown("""
    Sebbene questo mito sia globalmente condiviso da quasi tutti coloro che praticano lo sport, esso rimane una sensazione "a pelle", soggettiva. Dal punto di vista statistico infatti, molti studi vanno a confutare questa tesi, sostenendo che l'effetto degli esiti precedenti al tiro non ne influenzino la probabilità di successo.
    L'applicazione va a verificare questo, mostrando per ogni giocatore che si desideri, la percentuale di realizzazione di un tiro dividendole secondo le sequenze dei tiri precedenti, distinguendo quindi i casi di "serie positive e negative", oltre che statistiche generali dei giocatori per comprendere la bravura generale del giocatore.
    """)


    col3, col4=st.columns(2)
    with col3:
        st.markdown("""
        ### Percentuali Condizionate
Va ad analizzare quanto scritto nella premessa, ossia divide i tiri secondo 2 variabili: esito del tiro (**C**, canestro o **E**, errore) e la sequenza degli esiti dei tiri precedenti, fino a un massimo di 3. Per esempio, un errore preceduto da 2 canestri e un errore
sarà nella colonna **E** e nella riga **CCE**.
                    
Per ogni sequenza si calcola la **FG%**, percentuale di tiro, ossia la probabilità di successo di un tiro preceduto da quella sequenza di esiti. Secondo il mito della mano calda, dunque la **fg%** di una sequenza positiva (tiro subito precedente=canestro) dovrebbe sempre essere maggiore di quella di una sequenza negativa (=errore).

Per facilitare l'analisi per ogni giocatore c'è un grafico, dove l'asse X rappresenta la lunghezza della sequenza (per esempio, al terzo tiro avrà lunghezza 2), l'asse Y la percentuale della sequenza e il colore del pallino se la sequenza è positiva (verde), negativa (rosso) oppure nulla,
quindi il primo tiro di una partita (bianco). Se il grafico confermasse il mito, a parità di X, i pallini verdi sarebbero sempre sopra i pallini rossi.                    
""")
    with col4:
        exampledf=ds.updated_player_events_df("LaMelo Ball")
        st.dataframe(exampledf)
        st.altair_chart(gr.sequence_graph(exampledf), use_container_width=True)



    st.markdown(""" ### STATISTICHE GENERALI 
Va a dare una panoramica generale del giocatore mostrando canestri, errori e percentuale del campo medi per partita, senza condizioni dalle sequenze. 

Introduce anche le "streaks", ossia tutte le volte che 3 tiri consecutivi hanno lo stesso esito. che siano errori o canestri. Un'elevato numero di streaks indica che il giocatore è più soggetto agli effetti della mano calda e mano fredda.

Il grafico mostra la serie temporale di tutte le statistiche partita per partita. Inoltre, premendo il pulsante sotto, si può vedere per ogni partita l'esito e l'andamento della percentuale tiro per tiro, dove il pallino verde è un canestro (make) e il pallino rosso è un errore. (miss)
       """ )


    st.altair_chart(gr.gameforgame_stats_graph("LaMelo Ball"), use_container_width=True) 

    exampleevents=ds.player_modifiedevents_list("0022401217", "Jordan Poole")
    st.altair_chart(gr.singlegame_fg_graph(exampleevents), use_container_width=True)
    
    st.markdown(""" Per avere un termine di paragone:
                
- un giocatore di media importanza prende tra i 10 e i 15 tiri per partita, quelli più importanti superano anche i 20 mentre altri possono prenderne anche meno di 5;
                
- la percentuale media indicativa è 45%, una percentuale sotto il 40% è considerata pessima mentre sopra il 50% è ottima. 
    """)

    col5, col6=st.columns(2)
    with col5:
        st.markdown("""### STATISTICHE TOP 5
Mostra le ultime partite giocate dai 5 giocatori migliori per media punti segnati a partita, una delle statistiche più rappresentative per la nostra analisi:
essendo quelli che segnano di più sono probabilmente anche quelli che si prendono più tiri a partita, quindi la quantità di dati è più grande e perciò l'analisi viene approfondita di più.

Per ogni partita viene mostrato il gamelog completo con tutte le statistiche ufficiali NBA e il grafico dell'andamento della percentuale tiro per tiro.

Alla fine inoltre c'è un grafico a barre che confronta tutte e 5 le partite con canestri in verde, errori in rosso e streaks in giallo.""")
    
    with col6:
        st.image("https://www.sisal.it/content/dam/new-dam/italy/canali/sisal-it/scommesse/blog/2023/febbraio/nba-all-star-game-2023.jpg/_jcr_content/renditions/original",
                 caption="LeBron James nell'All Star Game, evento annuale dove si sfidano i migliori giocatori della stagione in corso")
        
    return_home_button()


elif st.session_state.page == "Percentuali Condizionate":
    st.markdown("<h1 style='text-align: center;'> Percentuali Condizionate</h1>", unsafe_allow_html=True)
    requestedplayer=st.text_input("Scrivi il giocatore desiderato e premi invio")
    st.divider()
    if requestedplayer:
        df=ds.updated_player_events_df(requestedplayer)
        if df is None:
            st.write("Spiacenti! Il giocatore desiderato non esiste. Controlla se lo hai scritto bene!")
        else:
            col1, col2, col3=st.columns(3)
            with col2:
                st.write("Giocatore scelto:", requestedplayer)
                st.image(v.show_player_photo(requestedplayer), width=275)
            st.divider()
            col4, col5=st.columns(2)
            with col4:
                st.markdown("""Vengono divisi i tiri secondo 2 variabili: esito del tiro (**C**, canestro o **E**, errore) e la sequenza degli esiti dei tiri precedenti.
                            
Per ogni sequenza si calcola la **FG%**, percentuale di tiro, ossia la probabilità di successo di un tiro preceduto da quella sequenza di esiti.
                            
Ricorda: una percentuale normale è tra il 40 e il 50%, sotto è molto bassa e sopra è molto alta. Essendo casi di sequenze singole, è probabile che i dati varino molto da sequenza a sequenza.""")
            with col5:
                st.dataframe(df)
            st.divider()
            st.markdown("""Nel grafico, l'asse X rappresenta la lunghezza della sequenza (per esempio, al terzo tiro avrà lunghezza 2), l'asse Y la percentuale della sequenza e il colore del pallino
se la sequenza è positiva (verde), negativa (rosso) oppure nulla, quindi il primo tiro di una partita (bianco).""")

            st.altair_chart(gr.sequence_graph(df))
    
    st.divider()
    return_home_button()

elif st.session_state.page == "Statistiche Generali":
    st.markdown("<h1 style='text-align: center;'> Statistiche Generali</h1>", unsafe_allow_html=True)
    requestedplayer=st.text_input("Scrivi il giocatore desiderato e premi invio")
    st.divider()
    if requestedplayer:
        df=ds.updated_player_events_df(requestedplayer)
        if df is None:
            st.write("Spiacenti! Il giocatore desiderato non esiste. Controlla se lo hai scritto bene!")
        else:
            col1, col2, col3=st.columns(3)
            with col2:
                st.write("Giocatore scelto:", requestedplayer)
                st.image(v.show_player_photo(requestedplayer), width=275)
            st.divider()
            df=ds.total_stats_df(requestedplayer)
            makes, misses, streaks, fgs = ds.summary_stats(df)
            st.markdown("### Statistiche medie per partita")
            st.write(f"Canestri: {makes}, Errori: {misses}, Streaks: {streaks}") 
            st.write(f"Percentuale dal campo: {fgs}%")
            st.divider()
            st.markdown("""Streaks = tutte le volte che 3 tiri consecutivi hanno lo stesso esito. che siano errori o canestri. Un'elevato numero di streaks indica che il giocatore è più soggetto agli effetti della mano calda e mano fredda.

Ricorda: una percentuale normale è tra il 40 e il 50%, sotto è molto bassa e sopra è molto alta.""")
            
            st.divider()
            st.text("""Il grafico mostra la serie temporale di tutte le statistiche partita per partita.""") 
            st.write("")
            st.altair_chart(gr.gameforgame_stats_graph(requestedplayer))
            st.divider()
            st.markdown("""Premendo il pulsante sotto, si può vedere per ogni partita l'esito e l'andamento della percentuale tiro per tiro, dove il pallino verde è un canestro (make) e il pallino rosso è un errore (miss).""")
            st.button("Premi per vedere la serie storica dei tiri di tutte le partite", on_click=lambda: single_game_graph_show(requestedplayer))

    st.divider()
    return_home_button()

elif st.session_state.page == "Statistiche Top 5":
    st.markdown("<h1 style='text-align: center;'> Statistiche Top 5 </h1>", unsafe_allow_html=True)
    
    top_list=v.get_top_scorers_names()
    statslist=[]
    for player in top_list:
        st.markdown(f"<h3 style='text-align: center;'>{player}</h3>", unsafe_allow_html=True)
        st.markdown(
        f"<div style='text-align: center;'><img src='{v.show_player_photo(player)}' width='400'/></div>",
        unsafe_allow_html=True)
        st.divider()
        logs = ds.player_gamelogs_df(player)
        lastlog = ds.last_gamelog(player)
        st.markdown("""### Ultima Partita
        
Gamelog completo con tutte le statistiche ufficiali NBA""")        
        st.write(lastlog.select(lastlog.columns[3:-1]))
        st.divider()
        game_id=lastlog[0, "Game_ID"]
        events=ds.player_modifiedevents_list(game_id, player)
        st.write("Andamento della percentuale tiro per tiro, pallino verde = canestro (make), pallino rosso = errore (miss).")
        st.altair_chart(gr.singlegame_fg_graph(events))
        st.divider()
        st.divider()
        c, e, s, fg = ds.single_game_stats(events)
        playerlist=[player, c, e, s]
        statslist.append(playerlist)

    st.write("Grafico a barre che confronta tutte e 5 le partite con canestri (makes), errori (misses) e streaks.")
    st.altair_chart(gr.top5_graph(statslist), use_container_width=True)
    
    return_home_button()
    