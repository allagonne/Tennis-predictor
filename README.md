<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][https://github.com/allagonne, https://github.com/gonzaloetjo, https://github.com/hungthang172]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://media.istockphoto.com/vectors/tennis-balls-vector-id1162635988?k=6&m=1162635988&s=612x612&w=0&h=PW0rFxvw6z2M2IYQmSRFLTMTjrSYxlR1y1XhBi-M2rM=">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Tennis-Predictor</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/allagonne/Tennis-predictor/tree/main/Python/Models"><strong>Explore the models »</strong></a>
    <br />
    <br />
    <a href="https://github.com/allagonne/Tennis-predictor/tree/main/Python/Match-Methods">Explore Data-Preparation</a>
    ·
    <a href="https://github.com/allagonne/Tennis-predictor/tree/main/Data">Explor Data</a>
    ·
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The goal of this project is to be able to predict with certain precision the winner of a professional ATP match.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:



### Built With

* [Python](https://www.python.org/)
* [Pandas](https://pandas.pydata.org/)
* [Keras](https://keras.io/)
* [Tensorflow](https://www.tensorflow.org/)
* [sklearn](https://scikit-learn.org/)



<!-- GETTING STARTED -->
## Getting Started

We suggest to create a virtual environment for python and continue with the installation.


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/allagonne/Tennis-predictor.git
   ```

2. Install REQUIRMENT.txt packages
   ```sh
   python3 -m pip install -r requirements.txt
   ```




<!-- USAGE EXAMPLES -->
## Usage

Once Installed all requirements, run the main.py script to process data.

 ```sh
   python Python/Match-Methods/main.py
   ```

To use the different models you can run:

1. KNN
   ```sh
   python Python/Models/KNN.py
   ```
2. LogReg
   ```sh
   python Python/Models/LogReg.py
   ```
3. NN
   ```sh
   python Python/Models/NN.py
   ```
4. LSTM
   ```sh
   python Python/Models/LSTM.py
   ```
5. SVM
   ```sh
   python Python/Models/SVM.py
   ```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/tennis-predictor`)
3. Commit your Changes (`git commit -m 'Add some features'`)
4. Push to the Branch (`git push origin feature/tennis-predictor`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

Data:
Tennis databases, files, and algorithms by Jeff Sackmann / Tennis Abstract is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
Based on a work at https://github.com/JeffSackmann.



<!-- CONTACT -->
## Contact

Thang Nguyen - nguyenhungthang@gmail.com
Gonzalo Etse - gonzaloetjo@gmail.com.com
Arnaud Llagonne - allagonne@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Paper by Sascha Wilkens: Sports Prediction and Betting Models in the Machine Learning Age: The Case of Tennis](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3506302)
* [JackSackman ATP Data](https://github.com/JeffSackmann/tennis_atp)
* [ATP Official Data](https://www.atptour.com/en/stats)



