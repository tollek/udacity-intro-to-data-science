import math
import numpy
import pandas
import statsmodels.api as sm
import matplotlib.pyplot as plt

def custom_heuristic(file_path):
    '''
    You are given a list of Titantic passengers and their associated
    information. More information about the data can be seen at the link below:
    http://www.kaggle.com/c/titanic-gettingStarted/data

    For this exercise, you need to write a custom heuristic that will take
    in some combination of the passenger's attributes and predict if the passenger
    survived the Titanic diaster.

    Can your custom heuristic beat 80% accuracy?
    
    The available attributes are:
    Pclass          Passenger Class
                    (1 = 1st; 2 = 2nd; 3 = 3rd)
    Name            Name
    Sex             Sex
    Age             Age
    SibSp           Number of Siblings/Spouses Aboard
    Parch           Number of Parents/Children Aboard
    Ticket          Ticket Number
    Fare            Passenger Fare
    Cabin           Cabin
    Embarked        Port of Embarkation
                    (C = Cherbourg; Q = Queenstown; S = Southampton)
                    
    SPECIAL NOTES:
    Pclass is a proxy for socioeconomic status (SES)
    1st ~ Upper; 2nd ~ Middle; 3rd ~ Lower

    Age is in years; fractional if age less than one
    If the age is estimated, it is in the form xx.5

    With respect to the family relation variables (i.e. SibSp and Parch)
    some relations were ignored. The following are the definitions used
    for SibSp and Parch.

    Sibling:  brother, sister, stepbrother, or stepsister of passenger aboard Titanic
    Spouse:   husband or wife of passenger aboard Titanic (mistresses and fiancees ignored)
    Parent:   mother or father of passenger aboard Titanic
    Child:    son, daughter, stepson, or stepdaughter of passenger aboard Titanic
    
    Write your prediction back into the "predictions" dictionary. The
    key of the dictionary should be the passenger's id (which can be accessed
    via passenger["PassengerId"]) and the associating value should be 1 if the
    passenger survvied or 0 otherwise. 

    For example, if a passenger is predicted to have survived:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 1

    And if a passenger is predicted to have perished in the disaster:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 0
    
    You can also look at the Titantic data that you will be working with
    at the link below:
    https://www.dropbox.com/s/r5f9aos8p9ri9sa/titanic_data.csv
    '''

    cols = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
    cols.remove('PassengerId')
    cols.remove('Survived')
    cols.remove('Name')
    # Ticket?
    cols.remove('Ticket')

    # Bucketize age
    df = pandas.read_csv(file_path)
    df['Age'].fillna(-1, inplace=True)
    df['AgeBucket'] = pandas.Series('', index=df.index)
    for idx, row in df.iterrows():
        age = row['Age']
        age_bucket = 'c'
        if age < 18:
            age_bucket = 'young'
        elif age < 25:
            age_bucket = 'midyoung'
        elif age < 40:
            age_bucket = 'midmid'
        else:
            age_bucket = 'old'
        df.loc[idx, 'AgeBucket'] = age_bucket
    # After AgeBucket is added, replace the Age with Bucket
    cols.remove('Age')
    cols.append('AgeBucket')

    # Replace cabin with first char
    df['Deck'] = pandas.Series('', index=df.index)
    for idx, row in df.iterrows():
        cabin = row['Cabin']
        if not pandas.isnull(cabin):
            df.loc[idx, 'Deck'] = cabin[0]
    cols.remove('Cabin')
    cols.append('Deck')

    # Bucketize fare
    df['Fare'].fillna(-1, inplace=True)
    df['FareBucket'] = pandas.Series(0, index=df.index)
    for idx, row in df.iterrows():
        fare = row['Fare']
        # Cap to makes bucketizing look nicer
        if fare > 100:
            df.loc[idx, 'Fare'] = 100

        fare_bucket = ''
        if fare <= 10:
            fare_bucket = 10
        elif fare <= 20:
            fare_bucket = 20
        elif fare <= 30:
            fare_bucket = 30
        elif fare <= 40:
            fare_bucket = 40
        else:
            fare_bucket = 100
        df.loc[idx, 'FareBucket'] = fare_bucket
    cols.remove('Fare')
    cols.append('FareBucket')


    # Print data relations
    features = []
    for i, coli in enumerate(cols):
        for j, colj in enumerate(cols):
            if i <= j:
                features.append([coli, colj])
                # features.append([coli, colj, 'Sex'])
    features = []
    #x = df[(df['Sex'] == 'male') & (df['Deck'] == 'E') & (df['AgeBucket'] == 'midmid')]

    survivor_threshold = 0.8
    base_threshold = 0
    for f in features:
                print "--------------------------------------------------------------"
                print f
                predictions = {}

                for passenger_index, passenger in df.iterrows():
                    key = ''
                    for k in f:
                        v = passenger[k]
                        key = key + ' ' + str(v)

                    predictions.setdefault(key, [0, 0])
                    predictions[key][0] += passenger['Survived']
                    predictions[key][1] += 1

                # Print the stats for features list
                # print ', '.join(df.columns)
                # print predictions
                for k in sorted(predictions.keys()):
                    v = predictions[k]
                    survivor = 1.0 * v[0] /  v[1]
                    base = v[1]
                    if survivor < survivor_threshold or base < base_threshold or 'female' in k:
                        continue
                    print '%s => %.2f (%d)' % (k, (1.0 * v[0] /  v[1]), v[1])

    # Observations:
    # PREDICTION female in [1, 2] class => 97, 92%
    # PREDICTION female with SbSp <= 2 [0.79, 0.75, 0.77]
    # PREDICTION female not from S [69%, against C, Q]
    # PREDICTION decks: B, D, E
    # TODO: fare: bucketize


    total_survivors = 0
    predictions = {}
    # df = pandas.read_csv(file_path)
    for passenger_index, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']
        survivor = 0

        sex = passenger['Sex']
        if sex == 'female':
            # 1 or 2nd class?
            if passenger['Pclass'] in [1, 2]:
                survivor = 1
            # Embarked in 'C' (Cherbourg)?
            if passenger['Embarked'] == 'C':
                survivor = 1
            if passenger['Deck'] in ['B', 'C', 'D', 'E']:
                survivor = 1
            if passenger['FareBucket'] == 100:
                survivor = 1

        # Bunch of findings
        if passenger['Pclass'] == 2 and passenger['Parch'] == 2:
            survivor = 1
        if passenger['SibSp'] == 1 and passenger['Deck'] in ['B', 'D']:
            survivor = 1
        if passenger['Parch'] == 2 and passenger['AgeBucket'] == 'midyoung':
            survivor = 1
        if passenger['Embarked'] == 'C' and passenger['Deck'] == 'D':
            survivor = 1
        if passenger['AgeBucket'] == 'midmid' and passenger['Deck'] in ['B', 'D']:
            survivor = 1
        if passenger['Sex'] == 'male' and passenger['Deck'] in ['E'] and passenger['AgeBucket'] == 'midmid':
            survivor = 1



        predictions[passenger_id] = survivor
        if survivor:
            total_survivors = total_survivors + 1

    print 'prediction rate: ', total_survivors, len(predictions)
    accurate = 0
    for _, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']
        prediction = predictions[passenger_id]
        if prediction == passenger['Survived']:
            accurate = accurate + 1
    #survived = sum(df['Survived'] == 1)
    print 'accuracy: ', (1.0 * accurate / len(predictions))

    return predictions


#custom_heuristic('./kaggle_titanic_train.csv')

# SUBMITTED CODE:
#     passenger_id = passenger['PassengerId']
#
#     # Set custom columns
#     passenger['Deck'] = ''
#     if not pandas.isnull(passenger['Cabin']):
#         passenger['Deck'] = passenger['Cabin'][0]
#
#     passenger['AgeBucket'] = ''
#     age = passenger['Age']
#     age_bucket = 'c'
#     if age < 18:
#         age_bucket = 'young'
#     elif age < 25:
#         age_bucket = 'midyoung'
#     elif age < 40:
#         age_bucket = 'midmid'
#     else:
#         age_bucket = 'old'
#     passenger['AgeBucket'] = age_bucket
#
#
#     survivor = 0
#
#     sex = passenger['Sex']
#     if sex == 'female':
#         # 1 or 2nd class?
#         if passenger['Pclass'] in [1, 2]:
#             survivor = 1
#         # Embarked in 'C' (Cherbourg)?
#         if passenger['Embarked'] == 'C':
#             survivor = 1
#         if passenger['Deck'] in ['B', 'C', 'D', 'E']:
#             survivor = 1
#         if passenger['Fare'] >= 40:
#             survivor = 1
#
#     # Bunch of findings
#     if passenger['Pclass'] == 2 and passenger['Parch'] == 2:
#         survivor = 1
#     if passenger['SibSp'] == 1 and passenger['Deck'] in ['B', 'D']:
#         survivor = 1
#     if passenger['Parch'] == 2 and passenger['AgeBucket'] == 'midyoung':
#         survivor = 1
#     if passenger['Embarked'] == 'C' and passenger['Deck'] == 'D':
#         survivor = 1
#     if passenger['AgeBucket'] == 'midmid' and passenger['Deck'] in ['B', 'D']:
#         survivor = 1
#     if passenger['Sex'] == 'male' and passenger['Deck'] in ['E'] and passenger['AgeBucket'] == 'midmid':
#         survivor = 1
#
#     predictions[passenger_id] = survivor