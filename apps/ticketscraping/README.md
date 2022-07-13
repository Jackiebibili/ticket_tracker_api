# TM QuickPicks 4.0 API Return Data Schema

```
{
   "meta": {
      "modified": ISOString,
      "expired": ISOString
   },
   "eventId": string,
   "offset": number,
   "total": number,
   "picks": {
      "type": "seat",
      "selection": "resale" or "standard",
      "quality": float < 1,
      "section": string,
      "row": string of number,
      "offerGroups": [
            {
               "offers": [
                  offerIds in string
               ],
               "places": [
                  placeIds in string
               ],
               "seats": [
                  seatIds in string
               ],
               "coordinates": []
            }
      ],
      "area": string,
      "descriptionId": string,
      "maxQuantity": number of seats,
      "shapes": unknown,
   }[],
   
   "places": {}[], //ToDo

   "_embedded": {
      "offer": {
         "meta": {
            "modified": ISOString,
            "expires": ISOString
         },
         "offerId": string,
         "rank": 0,
         "online": bool,
         "protected": bool,
         "rollup": bool,
         "inventoryType": "resale" or "primary",
         "offerType": "standard",
         "listingId": string,
         "listingVersionId": string,
         "currency": string,
         "listPrice": number,
         "faceValue": number,
         "totalPrice": number,
         "noChargesPrice": number,
         "charges": [
            {
               "reason": "service",
               "type": "fee",
               "amount": number
            }
         ],
         "sellableQuantities": [
            numbers
         ],
         "section": string,
         "row": string,
         "seatFrom": string,
         "seatTo": string,
         "ticketTypeId": string,
      }[]
   }
}
```
