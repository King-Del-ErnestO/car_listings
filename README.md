
<div align="center">

  <h3 align="center">Car Listings</h3>

  <p align="center">
    The Car listings dapp documentation.
  </p>
</div>

## About
<p>
    Car Listings is decentralized application (dapp) powered by <a href="https://docs.cartesi.io/cartesi-rollups/1.3/">cartesi</a> rollups technology.
</p>
<p> 
    It's a simple dapp application that utilizes the power of Cartesi rollups to allow users list cars for sale everyone to see.
</p>

## Getting Started

Below you'll find instructions on how setting up this dapp locally.

### Prerequisites

Here are some packages you need to have installed on your PC:

* [nodejs](https://nodejs.org/en), [npm](https://docs.npmjs.com/cli/v10/configuring-npm/install), [yarn](https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable) 

* [docker](https://docs.docker.com/get-docker/)

* [cartesi-cli](https://docs.cartesi.io/cartesi-rollups/1.3/development/migration/#install-cartesi-cli)
  ```sh
  npm install -g @cartesi/cli
  ```

### Installation

1. Clone this repo
   ```sh
   https://github.com/King-Del-ErnestO/car_listings.git
   ```
2. Install Python packages
   ```sh
   pip  install requirements.txt
   ```
3. Build and run the dapp via `cartesi-cli`
   ```sh
   cartesi build 
   ```
   and
   ```sh
   cartesi run 
   ```

## Usage

Here you can access the examples of dapp communication and resources consume.

There are these resources available on this dapp:

### Advanced handlers
* #### list car with just car name
  ```py
    desc — list a car with just car name and/or description in a string
    payload — String/Hex
  ```
  String example
  ```text
    FORD
  ```
  Hex example
  ``` 
  0x464f5244
  ```
  interact
    - *via `cartesi cli`*, access your terminal in another window and input these instructions below:
  
    ```sh
    cartesi send generic \
        --dapp=0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e \
        --chain-id=31337 \
        --rpc-url=http://127.0.0.1:8545 \
        --mnemonic-passphrase='test test test test test test test test test test test junk' \
        --input=0x464f5244
    ```


 
* #### List car
  ```js
    description — list car with full parameters
    param required — {name: string, price: int, desc: string}
  ```
  data sample
  ```json
    { 
        "name":"Ford", 
        "price":2000, 
        "desc":"Luxury Sports Car"
  
    }
  ```
  hex sample
  ``` 
  0x7b226e616d65223a22466f7264222c20227072696365223a323030302c202264657363223a224c75787572792053706f72747320436172227d
  ``` 
  interact
    - *via `cartesi cli`*, access your terminal in another window and input these instructions below:
  
    ```sh
    cartesi send generic \
        --dapp=0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e \
        --chain-id=31337 \
        --rpc-url=http://127.0.0.1:8545 \
        --mnemonic-passphrase='test test test test test test test test test test test junk' \
        --input=0x7b226e616d65223a22466f7264222c20227072696365223a323030302c202264657363223a224c75787572792053706f72747320436172227d
    ```
    - *via `cast`*, access your terminal in another window and input this single line instruction below:


### Inspect handlers 
* #### getAllCars
  ```js
    description — get all cars listed.
  ```
  returned hex sample
  ```json
    {
        "status": "Accepted",
        "exception_payload": null,
        "reports": [
            {
                "payload": "0x..."
            }
        ],
        "processed_input_count": 2
    }
  ```
  converted payload sample
  ```json 
    [
        {
            "id": 1, 
            "lister": "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266", 
            "car_name": "Ford", 
            "listing_ts": "2024-08-02 18:31:15", 
            "block_num": 515}
    ]

  ```
  interact
    - access the cartesi inspect endpoint on your browser
  ```sh 
  http://localhost:8080/inspect/getAllCars
  ```

* #### getcar/<_id>
  ```js
    description — get a listed car by given id.
    path parameter — car id (int)
  ```
  returned hex sample
  ```json
    {
        "status": "Accepted",
        "exception_payload": null,
        "reports": [
            {
                "payload": "0x..."
            }
        ],
        "processed_input_count": 2
    }
  ```
  converted payload sample
  ```json 
    {
        "id": 2, 
        "lister": "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266", 
        "car_name": "Cheveron", 
        "listing_ts": "2024-08-02 18:31:15", 
        "block_num": 515
    }
  ```
  interact
    - access the cartesi inspect endpoint on your browser
  ```sh 
  http://localhost:8080/inspect/getcar/2
  ```

* #### totallisting
  ```js
    description — get the total number of cars listed
  ```
  returned hex sample
  ```json
    {
        "status": "Accepted",
        "exception_payload": null,
        "reports": [
            {
                "payload": "0x..."
            }
        ],
        "processed_input_count": 2
    }
  ```
  converted payload sample
  ```json 
      3
  ```
  interact
    - access the cartesi inspect endpoint on your browser
  ```sh 
  http://localhost:8080/inspect/totallisting
  ```


## Converter
A python converter between json, string and hex format can be used. See instructions below:
* Edit converter.py file
* Uncomment the function you require by removing the # 
* For String to Hex: Replace "example" value under def string_to_hex() with string value you wish to convert
* For Hex to String: Replace "example" value under def hex_to_string() with hex you wish to convert
* For Json to Hex: Replace "example" value with under def json_to_hex() the json you wish to convert
* For Hex to Json: Replac "example" value with under def hex_to_json() hex you wish to convert

#### RUN in terminal
```py
  python converter.py
```

## Contributing
We welcome contributions from the community! If you'd like to contribute to Car Listings, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive commit messages.
- Push your changes to your forked repository.
- Submit a pull request to the main repository.
- Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License
Car Listings is released under the MIT License.

## Acknowledgments
Car Listings is built on top of the Cartesi platform and utilizes various open-source libraries and tools. We would like to express our gratitude to the developers and contributors of these projects.