
import random
import os

def generate_bubbles():

  sequence = ""
  time = 1
  target = 0
  while time < 163:
    right = {"Time":float(time),
            "Name":"TargetRight" + str(target),
            "Position":{"x":round(random.uniform(-0.63, 0.63), 2),"y":round(random.uniform(0.5, 1.8),2),"z":0.5},
            "Rotation":{"x":0,"y":0,"z":0}}
    left = {"Time":float(time),
            "Name":"TargetLeft" + str(target),
            "Position":{"x":round(random.uniform(-0.63, 0.63),2),"y":round(random.uniform(0.5, 1.8),2),"z":0.5},
            "Rotation":{"x":0,"y":0,"z":0}}
    sequence += str(right).replace(" ", "").replace("'", '"') + ",\n" + str(left).replace(" ", "").replace("'", '"') + ",\n"
    time += 10
    target += 1
    target = target % 10
  sequence = sequence[:-2] + "\n"
  
  return '''{
"Game":
[
{"Name":"PartyRoom","PrefabName":"Balloons","Duration":170,"Platform":"Quest","Version":1.0}
],
"TargetsPrefabs":
[
{"Name":"TargetRight0","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight1","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight2","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight3","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight4","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight5","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight6","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight7","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight8","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetRight9","PrefabName":"Bubble","tag":"RightSide","active":true},
{"Name":"TargetLeft0","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft1","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft2","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft3","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft4","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft5","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft6","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft7","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft8","PrefabName":"Bubble","tag":"LeftSide","active":true},
{"Name":"TargetLeft9","PrefabName":"Bubble","tag":"LeftSide","active":true}
],
"Player":
[
{"Name":"Player","PrefabName":"PlayerBubbles","tag":"Player","active":true,"Position":{"x":0,"y":0,"z":0}}
],
"Music":
[
{"Name":"DB-04","Lenght":164.0}
],
"Environment":
[
{"Name":"SkyDome","PrefabName":"SkyDome","tag":"Environment","active":true,"Position":{"x":0,"y":-3.02,"z":2.55},"Rotation":{"x":0,"y":180,"z":0},"Scale":{"x":0.26,"y":0.55,"z":0.28},"SkyCicleSpeed":0.05}
],
"FX":
[
{"Name":"HitCorrect","PrefabName":"FX_Confetti_01","tag":"FX","position":{"x":0.0,"y":0.0,"z":0.0}},
{"Name":"HitInCorrect","PrefabName":"FX_Fireworks_01","tag":"FX","active":true,"position":{"x":0.0,"y":0.0,"z":0.0}}
],
"TargetsSequence":\n[\n''' + sequence + '''],
"Data":
[
{"Name":"HeadCenter","PrefabName":"CenterEyeAnchor","Actived":true,"Position":true,"Orientation":true,"Message":"01"},
{"Name":"HeadRight","PrefabName":"RightEyeAnchor","Actived":true,"Position":true,"Orientation":true,"Message":"02"},
{"Name":"HeadLeft","PrefabName":"LeftEyeAnchor","Actived":false,"Position":true,"Orientation":true,"Message":"03"},
{"Name":"RightHand","PrefabName":"RightHandAnchor","Actived":false,"Position":true,"Orientation":true,"Message":"04"},
{"Name":"LeftHand","PrefabName":"LeftHandAnchor","Actived":true,"Position":true,"Orientation":true,"Message":"05"},
{"Name":"Targets","PrefabName":"Targets","Actived":true,"Position":true,"Orientation":true,"Message":"07"},
{"Name":"TargetRight0","PrefabName":"TargetRight0","Actived":false,"Position":true,"Orientation":true,"Message":"08"},
{"Name":"TargetLeft0","PrefabName":"TargetLeft0","Actived":false,"Position":true,"Orientation":true,"Message":"09"},
{"Name":"TargetRight1","PrefabName":"TargetRight1","Actived":false,"Position":true,"Orientation":true,"Message":"10"},
{"Name":"TargetLeft1","PrefabName":"TargetLeft1","Actived":true,"Position":true,"Orientation":true,"Message":"11"},
{"Name":"TargetRight2","PrefabName":"TargetRight2","Actived":true,"Position":true,"Orientation":true,"Message":"12"},
{"Name":"TargetLeft2","PrefabName":"TargetLeft2","Actived":true,"Position":true,"Orientation":true,"Message":"13"},
{"Name":"TargetRight3","PrefabName":"TargetRight3","Actived":true,"Position":true,"Orientation":true,"Message":"14"},
{"Name":"TargetLeft3","PrefabName":"TargetLeft3","Actived":true,"Position":true,"Orientation":true,"Message":"15"},
{"Name":"TargetRight4","PrefabName":"TargetRight4","Actived":true,"Position":true,"Orientation":true,"Message":"16"},
{"Name":"TargetLeft4","PrefabName":"TargetLeft4","Actived":true,"Position":true,"Orientation":true,"Message":"17"},
{"Name":"TargetRight5","PrefabName":"TargetRight5","Actived":true,"Position":true,"Orientation":true,"Message":"18"},
{"Name":"TargetLeft5","PrefabName":"TargetLeft5","Actived":true,"Position":true,"Orientation":true,"Message":"19"},
{"Name":"TargetRight6","PrefabName":"TargetRight6","Actived":true,"Position":true,"Orientation":true,"Message":"20"},
{"Name":"TargetLeft6","PrefabName":"TargetLeft6","Actived":true,"Position":true,"Orientation":true,"Message":"21"},
{"Name":"TargetRight7","PrefabName":"TargetRight7","Actived":true,"Position":true,"Orientation":true,"Message":"22"},
{"Name":"TargetLeft7","PrefabName":"TargetLeft7","Actived":true,"Position":true,"Orientation":true,"Message":"23"},
{"Name":"TargetRight8","PrefabName":"TargetRight8","Activede":true,"Position":true,"Orientation":true,"Message":"24"},
{"Name":"TargetLeft8","PrefabName":"TargetLeft8","Actived":true,"Position":true,"Orientation":true,"Message":"25"},
{"Name":"TargetRight9","PrefabName":"TargetRight9","Actived":true,"Position":true,"Orientation":true,"Message":"26"},
{"Name":"TargetLeft9","PrefabName":"TargetLeft9","Actived":true,"Position":true,"Orientation":true,"Message":"270000"},
],
}'''