from model import model

# Insert evidence that train is delayed (Observed evidence)
predictions = model.predict_proba({
    "train": "delayed"
})

# calculate the probability for each event
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"\t{value}: ", end='')
            print("{:.4f}".format(probability))