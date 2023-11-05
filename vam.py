result_matrix = []
origin = []
destination  = []
matrix = []
need = []
availability = []

def reset_result_matrix():
    column = []
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            column.append(0)
        result_matrix.append(column.copy())
        column.clear()

def sum_without_none(iterable):
    result = 0
    for number in iterable:
        if number is not None:
            result += number
            print(result)
    return result

def insert_artificial_origin():
    origin.append('dummy')
    line = []
    for i in range(0, len(destination)):
        line.append(0)
    matrix.append(line)
    availability.append(sum(need) - sum(availability))

def insert_artificial_destination():
    destination.append('dummy')
    for line in matrix:
        line.append(999)
    need.append(sum(availability) - sum(need))

def calculate_penalties():
    origin_penalty = []
    destination_penalty = []
    column = []

    for i, line in enumerate(matrix):
        origin_penalty.append(difference_lower_costs(iterable_without_none(line.copy(), need)))

    for j in range(0, len(matrix[0])):
        for k in range(0, len(matrix)):
            column.append(matrix[k][j])
        destination_penalty.append(difference_lower_costs(iterable_without_none(column, availability)))
        column.clear()

    return [origin_penalty, destination_penalty]

def difference_lower_costs(iterable):

    best = min(iterable)
    iterable.remove(best)

    if len(iterable) == 0:
        return best

    alternative = min(iterable)

    return abs(alternative - best)

def get_column(index):
    column = []
    for j in range(0, len(matrix)):
        column.append(matrix[j][index])
    return column

def iterable_without_none(iterable, comparable=None):
    iterable_remove_none = []
    for i, x in enumerate(iterable):
        if comparable is not None:
            if comparable[i] is not None:
                iterable_remove_none.append(x)
        else:
            if iterable[i] is not None:
                iterable_remove_none.append(x)
    return iterable_remove_none

def find_lower_cell(origin_penalty, destination_penalty):
    result = []

    max_difference_origin = max(origin_penalty)
    max_difference_destination = max(destination_penalty)

    if max_difference_origin < max_difference_destination:
        index_max_difference = destination_penalty.index(max_difference_destination)
        result.append(index_max_difference)
        column = get_column(index_max_difference)
        lower_cost_value = min(iterable_without_none(column, availability))
        result.append(lower_cost_value)
        result.append(column.index(lower_cost_value))
    else:
        index_max_difference = origin_penalty.index(max_difference_origin)
        result.append(index_max_difference)
        line = matrix[index_max_difference]
        lower_cost_value = min(iterable_without_none(line, need))
        result.append(lower_cost_value)
        result.append(line.index(lower_cost_value))
        result.reverse()

    return result

def calculate_result():
    z = 0
    for i in range(0, len(result_matrix)):
        for j in range(0, len(result_matrix[0])):
            z += result_matrix[i][j]
    return z

print("========================================\n")
factory_count = int(input("Masukkan jumlah pabrik: "))
factories = []
for i in range(1, factory_count + 1):
    factory_name = input("Masukkan nama pabrik " + str(i) + ": ")
    factories.append("Pabrik " + factory_name)
print("\n========================================\n")

warehouse_count = int(input("Masukkan jumlah gudang: "))
warehouses = []
for warehouse in range(1, warehouse_count + 1):
    warehouse_name = input("Masukkan nama gudang " + str(warehouse) + ": ")
    warehouses.append("Gudang " + warehouse_name)
print("\n========================================\n")

warehouse_needs = []
for i in range(warehouse_count):
    warehouse_need = int(input("Masukkan kebutuhan " + warehouses[i] + ": "))
    warehouse_needs.append(warehouse_need)
print("\n========================================\n")

factory_capacity = []
for i in range(factory_count):
    capacity = int(input("Masukkan kapasitas " + factories[i] + ": "))
    factory_capacity.append(capacity)
print("\n========================================\n")
    
cost_matrix = []
for f in range(factory_count):
    array = []
    for w in range(warehouse_count):
        cost = int(input("Masukkan biaya transportasi dari " + factories[f] + " ke " + warehouses[w] + ": "))
        array.append(cost)
    cost_matrix.append(array)

origin = factories
destination = warehouses
matrix = cost_matrix
need = warehouse_needs
availability = factory_capacity

if sum(need) > sum(availability):
    insert_artificial_origin()
elif sum(availability) > sum(need):
    insert_artificial_destination()

reset_result_matrix()

while (sum_without_none(availability) + sum_without_none(need)) != 0:

    origin_penalty, destination_penalty = calculate_penalties()
    index_column_need, lower_cost_value, index_line_availability = find_lower_cell(
        origin_penalty, destination_penalty)

    value_availability = availability[index_line_availability]
    value_need = need[index_column_need]

    if value_need < value_availability:
        result_matrix[index_line_availability][index_column_need] = lower_cost_value * value_need
        for i in range(0, len(matrix)):
            matrix[i][index_column_need] = 0
        need[index_column_need] = None
        availability[index_line_availability] -= value_need
    else:
        result_matrix[index_line_availability][index_column_need] = lower_cost_value * value_availability
        for i in range(0, len(matrix[0])):
            matrix[index_line_availability][i] = 0
        availability[index_line_availability] = None
        need[index_column_need] -= value_availability
print("\n========================================\n")

print("Hasil matrix: ")
print(result_matrix)
print("Jadi biaya transportasi yang harus dikeluarkan: " + str(calculate_result()))


'''Berikut penjelasan tentang fungsi-fungsi dan struktur keseluruhan kode:

1. `reset_result_matrix()`: Fungsi ini menginisialisasi `result_matrix` sebagai matriks dengan semua elemen diatur ke 0. Ini membersihkan data sebelumnya dalam `result_matrix` dan mempersiapkannya untuk menyimpan rencana transportasi.

2. `sum_without_none(iterable)`: Fungsi ini menghitung jumlah elemen dalam sebuah iterable, tanpa menghitung nilai `None`. Ia mengulangi iterable, menambahkan nilai bukan `None`, dan mengembalikan hasilnya.

3. `insert_artificial_origin()`: Fungsi ini menambahkan asal buatan ('dummy') dan baris nol yang sesuai ke dalam matriks. Ini menyesuaikan ketersediaan dengan memastikan bahwa jumlah ketersediaan sama dengan jumlah permintaan.

4. `insert_artificial_destination()`: Fungsi ini menambahkan tujuan buatan ('dummy') dan kolom biaya tinggi (999 dalam hal ini) yang sesuai ke dalam matriks. Ini menyesuaikan permintaan dengan memastikan bahwa jumlah permintaan sama dengan jumlah ketersediaan.

5. `calculate_penalties()`: Fungsi ini menghitung hukuman untuk asal dan tujuan. Ini menghitung hukuman berdasarkan perbedaan dalam dua biaya transportasi terendah untuk setiap asal dan tujuan.

6. `difference_lower_costs(iterable)`: Fungsi ini menghitung perbedaan antara dua biaya terendah dalam iterable yang diberikan. Ia menghapus biaya terendah, menemukan biaya terendah berikutnya, dan mengembalikan selisih absolut.

7. `get_column(index)`: Fungsi ini mengambil kolom tertentu dari matriks berdasarkan indeks kolom yang diberikan.

8. `iterable_without_none(iterable, comparable=None)`: Fungsi ini menyaring nilai `None` dari sebuah iterable dan mengembalikan iterable yang baru. Jika `comparable` disediakan, ia menyaring berdasarkan kehadiran `None` dalam iterable yang dibandingkan.

9. `find_lower_cell(origin_penalty, destination_penalty)`: Fungsi ini mencari sel (pasangan asal-tujuan) dengan hukuman tertinggi, baik dari hukuman asal atau tujuan. Ia mengembalikan daftar yang berisi indeks sel, nilai biaya terendah, dan indeks baris atau kolom yang sesuai.

10. `calculate_result()`: Fungsi ini menghitung total biaya rencana transportasi yang tersimpan dalam `result_matrix` dan mengembalikan hasilnya.

Kode kemudian melanjutkan untuk menerima masukan pengguna tentang jumlah pabrik, nama-nama pabrik, jumlah gudang, nama-nama gudang, kebutuhan gudang, kapasitas pabrik, dan biaya transportasi. Kemudian, ia menyesuaikan masalah untuk memastikan pasokan sama dengan permintaan dengan menambahkan asal atau tujuan buatan. Setelah itu, ia secara berulang mencari sel dengan biaya terendah dan memperbarui rencana transportasi sampai semua permintaan dan pasokan terpenuhi.

Akhirnya, kode mencetak matriks hasil dan total biaya transportasi.''' 
