# -*- coding: utf-8 -*-
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from libraries import postpy as postpy
from libraries import reading_and_saving as rs
import preprocess as preprocess

DATA_PATH = ""


def read_data(DATA_PATH, list_of_letters):
    f = open(DATA_PATH, 'r', encoding='utf-8')
    text = f.read()
    text = text[:-2]
    f.close()
    table = text.split('\n')
    set_of_letters = set()

    for record in table: 
        tab_of_line = record.split(';')
        if(tab_of_line[1] != 'nie doszedl'):
            letter_1 = postpy.Letter_ext(rs.split_data(tab_of_line[0]), rs.split_data(tab_of_line[1]), tab_of_line[2], tab_of_line[3], tab_of_line[4], tab_of_line[5], tab_of_line[7], tab_of_line[6],tab_of_line[8],tab_of_line[9])
            a = len(set_of_letters)
            set_of_letters.add(letter_1.numer_przesylki)
            b = len(set_of_letters)
            if b > a: 
                if(letter_1.data_wyslania<letter_1.data_dotarcia):
                    if(letter_1.on_time!='2'): # if known type of letter
                        list_of_letters.append(letter_1)    


def main():
    list_of_letters = []
    read_data(DATA_PATH, list_of_letters)


    df = pd.DataFrame.from_records([l.to_dict() for l in list_of_letters])
    df = preprocess.preprocess_data_frame(df)

    categorical_cols_ORD = ['typ', 'granica_15']
    categorical_cols_OH = ['dzien_tygodnia', 'typ_placowki']
    numerical_cols = ['czas', 'dyst', 'godzina']

    numerical_transformer, categorical_ORD_transformer, categorical_OH_transformer = preprocess.get_transformers()
    preprocessor = preprocess.get_preprocessor(numerical_transformer, categorical_ORD_transformer, categorical_OH_transformer, numerical_cols, categorical_cols_ORD, categorical_cols_OH)


    X_train, X_valid, y_train, y_valid = preprocess.get_train_val_sets(df, preprocessor)

    model = keras.Sequential([
        layers.Dense(units=50, activation='relu', input_shape=[15]),
        layers.Dropout(0.05),
        layers.Dense(units=50, activation='relu'),
        layers.Dropout(0.05),
        layers.Dense(units=50, activation='relu'),
        layers.Dropout(0.05),
        layers.Dense(units=1),
    ])


    model.compile(
        optimizer="adam",
        loss="mae",
    )

    early_stopping = EarlyStopping(
        min_delta=0.0001,
        patience=30, 
        restore_best_weights=True,
    )


    history = model.fit(
        X_train, y_train,
        validation_data=(X_valid, y_valid),
        batch_size=32,
        epochs=200,
        callbacks=[early_stopping],
        verbose=1
    )

    history_df = pd.DataFrame(history.history)
    history_df.loc[:, ['loss', 'val_loss']].plot();
    print("Minimum validation loss: {}".format(history_df['val_loss'].min()))
    print("Gap between val: {}".format(history_df['val_loss'].iloc[-1]-history_df['loss'].iloc[-1]))


if __name__ == "__main__":
    main()
