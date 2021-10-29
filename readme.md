<h5>To gather the review data, open command prompt and run:<h5/>

    main.py

<h5>To execute test, run:<h5/>

    test.py

<h5>to display the top3 most suspicious reviews via simple anomaly detection:<h5/>
    this uses the ratio of positive:neutral words, as all the reviews have minimal negative words.
    <br/>
    it filters out reviews that have a pos/neu ratio less than mean+(1*stdev)
    <br/>

    find_suspect_reviews.py

<h5>to display the top3 most suspicious reviews via simple anomaly detection:<h5/>
    this uses machine learning to predict deceptive reviews.
    <br/>
    data from: https://www.kaggle.com/rtatman/deceptive-opinion-spam-corpus
    <br/>
    Then it uses the ratio of positive:neutral words, as all the reviews have minimal negative words.
    <br/>
    it filters out reviews that have a pos/neu ratio less than mean+(1*stdev)
    <br/>

    ml_detection.py