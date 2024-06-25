from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from requests.exceptions import ConnectionError

from app import contract, web3
from app.vote import blueprint


@blueprint.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    if contract.caller().on_going is False:
        return "<h1> ELECTION was ENDED </h1>"

    if request.method == "GET":
        return render_template("vote/vote.html")

    deputy = ["AANG", "KORRA", "ROKU"]
    vote_for_id = deputy.index(request.form["voteBtn"])
    try:
        tx_hash = contract.functions.vote_for(vote_for_id).transact(
            {
                "from": current_user.address,
                "gas": 3_000_000,
            }
        )
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction successful with hash: {tx_receipt}")
    except ConnectionError as e:
        print(e)
        return "<h1> Truffle RPC server not established yet"
    except ValueError as e:
        print(e)
        return "<h1>Already voted", "error</h1>"

    return redirect(url_for("vote.voted"))


@blueprint.route("/voted", methods=["GET", "POST"])
def voted():
    logout_user()
    return render_template("vote/voted.html")
