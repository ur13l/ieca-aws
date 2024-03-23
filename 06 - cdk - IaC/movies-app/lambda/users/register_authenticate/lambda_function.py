import json
# import psycopg2
# import bcrypt

def handler(event, context):
    # body = json.loads(event['body'])
    # nombre_completo = body['nombre_completo']
    # correo = body['correo']
    # contraseña_plana = body['contraseña']

    # # Conectarse a la base de datos
    # conn = psycopg2.connect("dbname='tu_base_de_datos' user='usuario' host='host_de_rds' password='contraseña' port='5432'")
    # cur = conn.cursor()

    # # Hashear la contraseña
    # contraseña_hash = bcrypt.hashpw(contraseña_plana.encode('utf-8'), bcrypt.gensalt())

    # # Insertar el nuevo usuario en la base de datos
    # try:
    #     cur.execute("INSERT INTO usuarios (nombre_completo, correo, contraseña_hash) VALUES (%s, %s, %s)",
    #                 (nombre_completo, correo, contraseña_hash))
    #     conn.commit()
    #     response = {
    #         'statusCode': 200,
    #         'body': json.dumps('Usuario registrado exitosamente.')
    #     }
    # except Exception as e:
    #     conn.rollback()
    #     response = {
    #         'statusCode': 400,
    #         'body': json.dumps(str(e))
    #     }
    # finally:
    #     cur.close()
    #     conn.close()

    # return response
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
