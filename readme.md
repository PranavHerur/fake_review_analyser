<h5>First thing is to have python installed, 2nd thing is to install requirements with:<h5/>
    
    pip install -r requirements.txt

<h5>To execute tests, run:<h5/>

    test.py

<h5>To gather the review data, open command prompt and run:<h5/>

    main.py

<h5>To display the top3 most suspicious reviews via simple anomaly detection:<h5/>
    This uses the ratio of positive:neutral words, as all the reviews have minimal negative words.
    <br/>
    Then it displays the reviews that have the highest pos/neu ratio
    <br/>

    find_suspect_reviews.py

<h5>To display the top3 most suspicious reviews via simple anomaly detection:<h5/>
    This uses machine learning to predict deceptive reviews.
    <br/>
    data from: https://www.kaggle.com/rtatman/deceptive-opinion-spam-corpus
    <br/>
    Then it uses the ratio of positive:neutral words, as all the reviews have minimal negative words.
    <br/>
    Then it displays the reviews that have the highest pos/neu ratio
    <br/>

    ml_detection.py