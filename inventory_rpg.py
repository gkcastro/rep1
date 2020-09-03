# inventory.py
stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
leftwid = 14
rightwid = 5

def displayInventory(inventory): #Função para imprimir o inventário 
    print("Inventory:".center(leftwid + rightwid, '-'))
    item_total = 0 #Inicializa o total de itens
    for k, v in inventory.items(): #Imprime a o item (key) e a quantidade (value) do dicionário
        print(k.ljust(leftwid, '.') + str(v).rjust(rightwid))
        item_total += v #Atualiza o total de itens
    print("Total number of items: " + str(item_total))
    print('--------------------------')

def addToInventory(inventory, addedItems):
    for i in addedItems:
        inventory.setdefault(i,0) #Quando achar um item novo, seta o valor para zero
        inventory[i] += 1 #Atualiza a quantidade do item
    return inventory

displayInventory(stuff)
addToInventory(stuff,dragonLoot)
displayInventory(stuff)