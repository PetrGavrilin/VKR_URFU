# -*- coding: utf-8 -*-
"""VKR_function.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ty8FBkkFRY_-gdq-1213kedIEgznh3QO
"""

def print_scores(y_test, y_predict, test_ = True):
  # функция для вывода основных показателей точности

  from sklearn.metrics import mean_squared_error as mse # метрика MSE от Scikit-learn
  from sklearn.metrics import r2_score # коэффициент детерминации  от Scikit-learn

  if test_:
    print('Ошибка на тестовых данных')
  else:
    print("Ошибка на полных данных")
  print('MSE: %.5f' % mse(y_test,y_predict))
  print('RMSE: %.5f' % mse(y_test,y_predict,squared=False))
  print('R2 : %.5f' %  r2_score(y_test,y_predict))



def plot_predict(Y, i_test, y_test_predict, y_all_predict, borders, text=""):
  # функция построения графика расхода с выделением точек значительного его изменения

    import matplotlib.pyplot as plt

    plt.figure(figsize=(18, 7))
    plt.title(f"Показания эталонного расходомера и предсказаний для {text}", fontsize=16)
    plt.xlabel("Номер измерения", fontsize=16)
    plt.ylabel("Расход, м\u00B3/ч.", fontsize=16)
    ax1 = plt.axes
    plt.plot(Y)
    plt.plot(y_all_predict, color="green", linewidth= 0.4)
    plt.plot(i_test, y_test_predict,'ro', ms = 1)

    for x in borders:
        plt.axline((x, Y.max()), (x, Y.min()), color="red", linewidth= 0.8)

    plt.legend(["Факт", "предсказания по всей выборке", "предсказания на тестовой выборке"], loc='upper left', prop={'size': 16})

    ax2 = plt.axes([0.5, 0.23, 0.35, 0.35])

    i = list(range(1200, 1300))
    i_test2 = []
    y_test_predict2 =[]
    for j in range(len(i_test)):
      if (i_test[j] >= 1200) & (i_test[j] < 1300):
        i_test2.append(i_test[j])
        y_test_predict2.append(y_test_predict[j])


    plt.xlabel("Номер измерения")
    plt.ylabel("Расход, м\u00B3/ч.")
    plt.plot(i,Y[i])
    plt.plot(i,y_all_predict[i], color="green", linewidth= 0.8)
    plt.plot(i_test2,y_test_predict2,'ro', ms = 4)

    plt.grid()

    plt.show()

    return None



def my_features_extraction(S):
  # функция извлечения признаков

  import tsfel
  from sklearn.feature_selection import VarianceThreshold
  from sklearn import preprocessing

  cfg_file = tsfel.get_features_by_domain()
  s = S.values.tolist()
  X = tsfel.time_series_features_extractor(cfg_file, s)

  # Удаление признаков с сильной корреляцией
  corr_features = tsfel.correlated_features(X)
  X.drop(corr_features, axis=1, inplace=True)

  # Удаление признаков с низкой дисперсией
  selector = VarianceThreshold()
  X = selector.fit_transform(X)

  #Нормализация
  scaler_up = preprocessing.StandardScaler()
  nX = scaler_up.fit_transform(X)

  return nX


def my_test_train_split(X, Y, borders, test_size=0.1):
  # функция разделения на обучающую и тренировочную выборку

  import random

  b1 = 0
  i_test = []
  l_ = len(Y)

  for i_s in borders:
    i_t = random.sample(range(b1, i_s), int(test_size*(i_s-b1)))
    i_test.extend(i_t)
    b1 = i_s

  i_t = random.sample(range(b1, l_), int(test_size*(l_-b1)))
  i_test.extend(i_t)
  i_test.sort()

  i_train = list(range(0,l_))
  for x1 in i_test:
    i_train.remove(x1)

  X_train = X[i_train,:]
  y_train = Y[i_train]

  X_test = X[i_test,:]
  y_test = Y[i_test]

  return X_train, y_train, X_test, y_test, i_test

def my_test_val_train_split(X, Y, borders, test_size=0.2, val_size=0.2):
  # функция разделения на обучающую, валидационную и тренировочную выборку

  import random

  b1 = 0
  i_test = []
  i_val = []
  l_ = len(Y)

  test_val_size = test_size+val_size*(1-test_size)

  for i_s in borders:
    i_t = random.sample(range(b1, i_s), int(test_val_size*(i_s-b1)))

    i_v = random.sample(i_t, int(len(i_t)*(val_size/test_val_size)))
    
    for x1 in i_v:
      i_t.remove(x1)

    i_test.extend(i_t)
    i_val.extend(i_v)
    b1 = i_s

  i_t = random.sample(range(b1, l_), int(test_val_size*(l_-b1)))

  i_v = random.sample(i_t, int(len(i_t)*(test_size/test_val_size)))

  for x1 in i_v:
    i_t.remove(x1)

  i_test.extend(i_t)
  i_val.extend(i_v)
  
  i_test.sort()
  i_val.sort()

  i_train = list(range(0,l_))
  for x1 in i_test:
    i_train.remove(x1)
  for x1 in i_val:
    i_train.remove(x1)

  X_train = X[i_train,:]
  y_train = Y[i_train]

  X_val = X[i_val,:]
  y_val = Y[i_val]

  X_test = X[i_test,:]
  y_test = Y[i_test]

  return X_train, y_train, i_train, X_val, y_val, i_val, X_test, y_test, i_test