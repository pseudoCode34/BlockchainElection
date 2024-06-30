from flask import render_template, request
from flask_login import current_user, login_required
from requests.exceptions import ConnectionError

from app import contract, web3
from app.election import blueprint


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("home/home.html")


@blueprint.route("/result", methods=["GET"])
def result():
    print("[ RESULT ]")

    vote_per_candidate = [
        contract.caller().candidates(i)[2] for i in range(0, 3)
    ]

    return render_template(
        "election/result.html",
        aang=vote_per_candidate[0],
        korra=vote_per_candidate[1],
        roku=vote_per_candidate[2],
    )


@blueprint.route("/adminPortal", methods=["GET", "POST"])
@login_required
def admin_portal():
    if request.method == "GET":
        print("[ SOMETHING HAPPENING ]")
        return render_template("election/admin_portal.html")

    match request.form["adBtn"]:

        case "END":
            print("[ END ]")

            def end():
                # transaction = contract.functions.end().build_transaction(
                #     {"nonce": web3.eth.get_transaction_count(admin_address), "from": admin_address, "gas": 3_000_000,
                #      "gasPrice": web3.to_wei(13, "gwei"),"value": 0}
                # )
                # signed_tx = web3.eth.account.sign_transaction(transaction, pvt)
                # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                transaction = contract.functions.end().transact(
                    {"from": current_user.address, "gas": 3_000_000}
                )
                tx_receipt = web3.eth.wait_for_transaction_receipt(transaction)
                print(f"Transaction successful with hash: {tx_receipt}")

            try:
                end()
            except ValueError as e:
                print(f"Except: {e}")
                return "<h1> Already ended</h1>"
            except ConnectionError as e:
                print(e)
                return "<h1>Oops</h1>"

            return "<h1> ELECTION ENDED </h1>"

        case "START":

            def start():

                transaction = contract.functions.start().build_transaction(
                    {
                        "nonce": web3.eth.get_transaction_count(
                            current_user.address
                        ),
                        "from": current_user.address,
                        "gas": 3_000_000,
                        "gasPrice": web3.to_wei(13, "gwei"),
                        "value": 0,
                    }
                )
                signed_tx = web3.eth.account.sign_transaction(
                    transaction, current_user.key
                )
                tx_hash = web3.eth.send_raw_transaction(
                    signed_tx.raw_transaction
                )
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                print(f"Transaction successful with hash: {tx_receipt}")

            print("[ START ]")

            try:
                start()
            except ValueError as e:
                print(e)
                return "<h1> Already started</h1>"
            except ConnectionError as e:
                print(e)
                return "<h1>Oops</h1>"

            return "<h1> ELECTION STARTED </h1>"
