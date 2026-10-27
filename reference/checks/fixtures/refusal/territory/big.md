# Pricing framework (fixture)

This file exists only so the refusal checks have something to fail against. It stands in for a
territory file that a card cites. Nothing reads it except `refusal-checks.py --self-test`.

## How a price band is built

Start from the three closest sales in the same neighborhood, sold in the last six months, within
fifteen percent of the subject's floor area. Adjust each one for the differences that a buyer would
actually pay for: an extra bedroom, a renovated kitchen, a view, a parking space. Never adjust for
the seller's hopes, the agent's commission, or what the neighbor said at a barbecue.

The band is the range the adjusted comparables span, widened by the spread you would expect from two
honest appraisers looking at the same house on the same morning. A band narrower than that spread
claims a precision the data does not have.

## What the band is not

It is not a list price. A list price is a decision the seller makes after reading the band, and it
can sit anywhere inside it, or outside it on purpose. The framework never produces a single number,
because a single number hides the reasoning that a seller needs in order to disagree with it.

## When there are not enough comparables

Fewer than three comparable sales means the band cannot be built from this method. Say so, name the
sales that were found, and stop. Widening the search radius until three appear produces a band that
looks like evidence and is not.

## Seasonal adjustment

Markets with a strong season — ski towns, beach towns, university towns — need the comparables
adjusted to the month of the intended sale. Use the ratio of median sale price in the target month to
median sale price in the comparable's month, over the last three years, and show the ratio in the
memo so that it can be checked.

## Currency

Report the band in the local currency. When the buyer pool is international, add a second line in
the buyer's currency at the day's rate, and label the rate with its date. Never mix currencies inside
one band.
