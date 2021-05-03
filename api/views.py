from django.shortcuts import render

# Create your views here.

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from.serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from .models import Artist, Album, Track
import base64





class ListArtist(APIView):

    serializer_class = serializers.ArtistSerializer

    def get(self, request, format=None):
        #an_apiview = [ "probando probando"]

        data_artistas = list(Artist.objects.values())
        #serializer = ArtistSerializer(artistas, many=True)
        dict_info = Artist.objects.values()

        #return Response({'message': an_apiview})
        return Response(data_artistas,status=status.HTTP_200_OK)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            #serializer.save()
            # PRIMERO RECIBIMOS LOS CAMPOS INGRESADOS EN EL FORM (pasados por el serializer)
            name = serializer.validated_data.get('name')
            age = serializer.validated_data.get('age')
            #albums = serializer.validated_data.get('albums')
            #tracks = serializer.validated_data.get('tracks')

            #confirmamos si existe el id:
            id_aux = base64.b64encode(name.encode()).decode()
            id_nuevo = id_aux[:22]

            try:
                artista_existente = Artist.objects.get(id=id_nuevo)

                #retornar existente
                dict_aux = dict()
                dict_aux["id"] = artista_existente.id
                dict_aux["name"] = artista_existente.name
                dict_aux["age"] = artista_existente.age
                dict_aux["albums"] = artista_existente.albums
                dict_aux["tracks"] = artista_existente.tracks
                dict_aux["self"] = artista_existente.self

                lista_final = []
                lista_final.append(dict_aux)
                return Response(dict_aux,status=status.HTTP_409_CONFLICT)
            except:
                pass
                
                
            # creamos una instancia del modelo Artist y asignamos valores
            new_artist = Artist()
            new_artist.name = name
            id_generado = base64.b64encode(name.encode()).decode()


            new_artist.id = id_generado[:22]
            new_artist.age = age
            new_artist.albums = f"https://t2integracion.herokuapp.com/artists/{new_artist.id}/albums"
            new_artist.tracks = f"https://t2integracion.herokuapp.com/artists/{new_artist.id}/tracks"
            new_artist.self = f"https://t2integracion.herokuapp.com/artists/{new_artist.id}"

            new_artist.save()


            dict_aux = dict()
            dict_aux["id"] = new_artist.id
            dict_aux["name"] = new_artist.name
            dict_aux["age"] = new_artist.age
            dict_aux["albums"] = new_artist.albums
            dict_aux["tracks"] = new_artist.tracks
            dict_aux["self"] = new_artist.self

            lista_final = []
            lista_final.append(dict_aux)

            #return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(dict_aux,status=status.HTTP_201_CREATED)


            #return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ArtistbyID(APIView):

    serializer_class = serializers.ArtistSerializer

    def get(self, request, pk):
        try:
            data_artista = Artist.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)


        data_artista = Artist.objects.get(id=pk)
        data_serialized = ArtistSerializer(data_artista)
        # agregamos la contraseña que no viene en el serializer
        dict_aux = dict(data_serialized.data)
        print("A")
        dict_data = dict() # name y age
        dict_data["id"] = data_artista.id
        print("B")
        dict_data["name"] = dict_aux["name"]
        print("c")
        dict_data["age"] = dict_aux["age"]
        print("D")
        dict_data["albums"] = data_artista.albums
        print("E")
        dict_data["tracks"] = data_artista.tracks
        print("F")
        dict_data["self"] = f"https://t2integracion.herokuapp.com/artists/{data_artista.id}"

        #return_data = list(dict_data)
        #print(return_data)
        lista_final = []
        lista_final.append(dict_data)
        return Response(dict_data,status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            artist_data = Artist.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        artist_data = Artist.objects.get(id=pk)
        artist_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AlbumbyID(APIView):
    serializer_class = serializers.AlbumSerializer

    def get(self, request, pk):

        try:
            data_artista = Artist.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)

        get_id = Artist.objects.get(id=pk)
        print(get_id) # Artist object (amFqamFqIGphamFqYQ==)



        try:
            # ojo son variossss
            list_aux = []
            data_album = Album.objects.filter(artist_id=get_id)
            for item in data_album:
                data_serialized = AlbumSerializer(item)

                dict_aux = dict(data_serialized.data)
                dict_data = dict()

                dict_data["id"] = item.id
                #print("1")
                dict_data["artist_id"] = item.artist_id_id
                #print("2")
                #name genre
                dict_data["name"] = dict_aux["name"]
                dict_data["genre"] = dict_aux["genre"]

                dict_data["artist"] = item.artist
                #print("3")
                dict_data["tracks"] = item.tracks
                #print("4")
                dict_data["self"] = f"https://t2integracion.herokuapp.com/albums/{item.id}"
                #print("5")
                
                list_aux.append(dict_data)
            return Response(list_aux, status=status.HTTP_200_OK)

            '''
            data_album = Album.objects.filter(id=get_id)

            print("pase")
            data_serialized = AlbumSerializer(data_album)
            print("pase2")
            dict_data = dict(data_serialized.data)
            print("pase3")
            dict_data["id"] = data_album.id
            print("pase4")

            return Response(dict_data)
            '''

        except:
            print("entre a error***")

            return Response({})

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        #serializer = serializers.AlbumSerializer(data=request.data)

        if serializer.is_valid():
            print("es valid")
            #serializer.save()
            # PRIMERO RECIBIMOS LOS CAMPOS INGRESADOS EN EL FORM (pasados por el serializer)
            #artist_id = serializer.validated_data.get('artist_id')
            name = serializer.validated_data.get('name')
            genre = serializer.validated_data.get('genre')
            #artist = serializer.validated_data.get('artist')
            #tracks = serializer.validated_data.get('tracks')
            # creamos una instancia del modelo Artist y asignamos valores

            # manejamos si esta malo el usuario
            try:
                artista_existente = Artist.objects.get(id=pk)
                
            except:
                return Response({},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # calculo id
            artista_creador = Artist.objects.get(id=pk)
            id_cadena = str(name)+":"+str(artista_creador)
            id_generado = base64.b64encode(id_cadena.encode()).decode()
            id_final = id_generado[:22]

            try:
                album_existente = Album.objects.get(id=id_final)
                #retornar existente
                dict_aux = dict()
                dict_aux["id"] = album_existente.id
                dict_aux["artist_id"] = artista_creador.id
                dict_aux["name"] = album_existente.name
                dict_aux["genre"] = album_existente.genre
                dict_aux["artist"] = album_existente.artist
                dict_aux["tracks"] = album_existente.tracks
                dict_aux["self"] = album_existente.self

                lista_final = []
                lista_final.append(dict_aux)




                return Response(dict_aux,status=status.HTTP_409_CONFLICT)
                
            except:
                
                # -------
                new_album = Album()

                new_album.name = name
                artista_creador = Artist.objects.get(id=pk)

                new_album.artist_id = artista_creador

                aux = str(artista_creador)

                #"<nombre_album>:<artist_id>
                id_cadena = str(name)+":"+str(aux)
                id_generado = base64.b64encode(id_cadena.encode()).decode()
                print(id_generado[:22])
                new_album.id =  id_generado[:22]

                #new_album.id = artista_creador

                new_album.genre = genre
                new_album.artist = f"https://t2integracion.herokuapp.com/artists/{artista_creador.id}"
                new_album.tracks = f"https://t2integracion.herokuapp.com/albums/{new_album.id}/tracks" 
                new_album.self = f"https://t2integracion.herokuapp.com/albums/{new_album.id}" 
                new_album.save()



                dict_aux = dict()
                dict_aux["id"] = new_album.id
                dict_aux["artist_id"] = artista_creador.id
                dict_aux["name"] = new_album.name
                dict_aux["genre"] = new_album.genre
                dict_aux["artist"] = new_album.artist
                dict_aux["tracks"] = new_album.tracks
                dict_aux["self"] = new_album.self

                lista_final = []
                lista_final.append(dict_aux)



                #return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(dict_aux,status=status.HTTP_201_CREATED)
        else:
            print("no es valid")
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ListAlbum(APIView):

    serializer_class = serializers.AlbumSerializer
    def get(self, request, format=None):
        #an_apiview = [ "probando probando"]

        #data_tracks = list(Track.objects.values())
        #serializer = ArtistSerializer(artistas, many=True)
        #--------
        lista_albums = list(Album.objects.values())
        lista_aux = []
        for item in lista_albums:
            #----
            aux = item["artist_id_id"]
            item["artist_id"] = aux
            del item["artist_id_id"]
            lista_aux.append(item)

        lista_ordenada = []
        for item in lista_aux:
            dict_aux = dict()
            dict_aux["id"] = item["id"]
            dict_aux["artist_id"] = item["artist_id"]
            dict_aux["name"] = item["name"]
            dict_aux["genre"] = item["genre"]
            dict_aux["artist"] = item["artist"] 
            dict_aux["tracks"] = item["tracks"]
            dict_aux["self"] = item["self"]

            lista_ordenada.append(dict_aux)

        #------

        #return Response({'message': an_apiview})
        #return Response(data_tracks)
        return Response(lista_ordenada,status=status.HTTP_200_OK)

    '''

    def get(self, request, format=None):
        #an_apiview = [ "probando probando"]

        data_albums = list(Album.objects.values())
        #serializer = ArtistSerializer(artistas, many=True)

        #return Response({'message': an_apiview})
        return Response(data_albums)
    '''


class OneAlbum(APIView):

    serializer_class = serializers.AlbumSerializer

    def get(self, request, pk):

        try:
            data_album = Album.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)


        data_album = Album.objects.get(id=pk)
        data_serialized = AlbumSerializer(data_album)
        # agregamos la contraseña que no viene en el serializer
        dict_aux = dict(data_serialized.data)
        print("A")
        dict_data = dict() # name y age
        dict_data["id"] = data_album.id
        print("B")
        dict_data["artist_id"] = data_album.artist_id_id
        print("c")
        dict_data["name"] = dict_aux["name"]
        print("D")
        dict_data["genre"] = dict_aux["genre"]

        dict_data["artist"] = data_album.artist

        print("E")
        dict_data["tracks"] = data_album.tracks
        print("F")
        dict_data["self"] = f"https://t2integracion.herokuapp.com/albums/{data_album.id}"

        #return_data = list(dict_data)
        #print(return_data)
        lista_final = list()
        lista_final.append(dict_data)
        return Response(lista_final,status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            album_data = Album.objects.get(id=pk)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        album_data = Album.objects.get(id=pk)
        album_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#------------------------------


class TrackbyId(APIView):


    serializer_class = serializers.TrackSerializer

    def get(self, request, pk):

        try:
            data_album = Album.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)

        get_id = Album.objects.get(id=pk)
        #print(get_id) # Artist object (amFqamFqIGphamFqYQ==)

        try:
            #print("entre al try")
            # ojo son variossss
            list_aux = []
            data_track = Track.objects.filter(album_id=get_id)
            #print("entre al try 2")
            #------
            for item in data_track:
                #print("entre al try 3")
                data_serialized = TrackSerializer(item)
                #print("entre al try 4")

                dict_aux = dict(data_serialized.data)
                dict_data = dict()
                #print("entre al try 5")

                dict_data["id"] = item.id
                #print("1")
                dict_data["album_id"] = item.album_id_id
                #print("2")
                #name genre
                dict_data["name"] = dict_aux["name"]
                dict_data["duration"] = dict_aux["duration"]

                dict_data["times_played"] = item.times_played
                #print("3")
                dict_data["artist"] = item.artist
                #print("4")
                dict_data["album"] = item.album
                dict_data["self"] = f"https://t2integracion.herokuapp.com/tracks/{item.id}"
                #print("5")

                
                list_aux.append(dict_data)
            return Response(list_aux,status=status.HTTP_200_OK)

            '''
            data_album = Album.objects.filter(id=get_id)

            print("pase")
            data_serialized = AlbumSerializer(data_album)
            print("pase2")
            dict_data = dict(data_serialized.data)
            print("pase3")
            dict_data["id"] = data_album.id
            print("pase4")

            return Response(dict_data)
            '''

        except:
            print("entre a error***")

            return Response({})

    def post(self, request, pk):

        serializer = self.serializer_class(data=request.data)
        #serializer = serializers.AlbumSerializer(data=request.data)

        if serializer.is_valid():
            print("es valid")
            #serializer.save()
            # PRIMERO RECIBIMOS LOS CAMPOS INGRESADOS EN EL FORM (pasados por el serializer)
            #artist_id = serializer.validated_data.get('artist_id')
            name = serializer.validated_data.get('name')
            duration = serializer.validated_data.get('duration')
            #artist = serializer.validated_data.get('artist')
            #tracks = serializer.validated_data.get('tracks')
            # creamos una instancia del modelo Artist y asignamos valores

            # manejamos si esta malo el usuario
            try:
                artista_existente = Album.objects.get(id=pk)
                
            except:

                return Response({},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # calculo id
            album_creador = Album.objects.get(id=pk)

            '''
            id_cadena = str(name)+":"+str(artista_creador)
            id_generado = base64.b64encode(id_cadena.encode()).decode()
            id_final = id_generado[:22]

            try:
                album_existente = Album.objects.get(id=id_final)
                return Response({},status=status.HTTP_409_CONFLICT)
                
            except:
                pass
            '''
            new_track = Track()

            new_track.name = name
            album_creador = Album.objects.get(id=pk)

            new_track.album_id = album_creador

            aux = str(album_creador)

            #"<nombre_album>:<artist_id>
            id_cadena = str(name)+":"+str(aux)
            id_generado = base64.b64encode(id_cadena.encode()).decode()
            print(id_generado[:22])
            new_track.id =  id_generado[:22]

            #new_album.id = artista_creador

            new_track.duration = duration
            #----

            instancia = album_creador.artist_id
            id_instancia = instancia.id

            #----
            #new_track.artist = f"https://t2integracion.herokuapp.com/artists/{album_creador.artist_id}"
            new_track.artist = f"https://t2integracion.herokuapp.com/artists/{id_instancia}"

            new_track.album = f"https://t2integracion.herokuapp.com/albums/{album_creador.id}" 
            new_track.self = f"https://t2integracion.herokuapp.com/tracks/{new_track.id}" 
            new_track.save()



            dict_aux = dict()
            dict_aux["id"] = new_track.id
            dict_aux["album_id"] = album_creador.id
            dict_aux["name"] = new_track.name
            dict_aux["duration"] = new_track.duration
            dict_aux["times_played"] = new_track.times_played
            dict_aux["artist"] = new_track.artist
            dict_aux["album"] = new_track.album
            dict_aux["self"] = new_track.self

            lista_final = []
            lista_final.append(dict_aux)



            #return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(dict_aux,status=status.HTTP_201_CREATED)



            #return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print("no es valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------
class ListTrack(APIView):

    serializer_class = serializers.TrackSerializer

    def get(self, request, format=None):
        #an_apiview = [ "probando probando"]

        #data_tracks = list(Track.objects.values())
        #serializer = ArtistSerializer(artistas, many=True)
        #--------
        lista_tracks = list(Track.objects.values())
        lista_aux = []
        for item in lista_tracks:
            aux = item["album_id_id"]
            item["album_id"] = aux
            del item["album_id_id"]
            lista_aux.append(item)

        lista_ordenada = []
        for item in lista_aux:
            dict_aux = dict()
            dict_aux["id"] = item["id"]
            dict_aux["album_id"] = item["album_id"]
            dict_aux["name"] = item["name"]
            dict_aux["duration"] = item["duration"]
            dict_aux["times_played"] = item["times_played"]
            dict_aux["artist"] = item["artist"] 
            dict_aux["album"] = item["album"]
            dict_aux["self"] = item["self"]

            lista_ordenada.append(dict_aux)

        #------

        #return Response({'message': an_apiview})
        #return Response(data_tracks)
        return Response(lista_ordenada,status=status.HTTP_200_OK)


#-------------------------------
class OneTrack(APIView):

    serializer_class = serializers.TrackSerializer

    def get(self, request, pk):

        try:
            data_track = Track.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)


        data_track = Track.objects.get(id=pk)

        data_serialized = TrackSerializer(data_track)
        # agregamos la contraseña que no viene en el serializer
        dict_aux = dict(data_serialized.data)
        print("A")
        dict_data = dict() # name y age

        dict_data["id"] = data_track.id
        print("B")
        dict_data["album_id"] = data_track.album_id_id
        print("c")
        dict_data["name"] = dict_aux["name"]
        print("D")
        dict_data["duration"] = dict_aux["duration"]

        dict_data["times_played"] = data_track.times_played

        print("E")

        #aux = data_track.artist_id
        #saux2 = aux.id

        dict_data["artist"] = data_track.artist
        #dict_data["artist"] = f"https://t2integracion.herokuapp.com/{data_track.album_id.}"

        print("F")
        dict_data["album"] = data_track.album

        dict_data["self"] = f"https://t2integracion.herokuapp.com/tracks/{data_track.id}"

        #return_data = list(dict_data)
        #print(return_data)
        lista_final = []
        lista_final.append(dict_data)
        return Response(lista_final,status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            track_data = Track.objects.get(id=pk)
            track_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #try:
            #eliminacion = track_data.delete()
            #if eliminacion:

                #return Response(status=status.HTTP_204_NO_CONTENT)
        #except:
            #return Response(status=status.HTTP_404_NOT_FOUND)


# ------

class TracksArtists(APIView):

    serializer_class = serializers.TrackSerializer

    def get(self, request, pk):

        try:
            data_artista = Artist.objects.get(id=pk)
        except:
            return Response({},status=status.HTTP_404_NOT_FOUND)

        get_id = Artist.objects.get(id=pk)
        #print(get_id) # Artist object (amFqamFqIGphamFqYQ==)

        try:
            # ojo son variossss
            list_aux = [] #json de los albumes del artista
            data_album = Album.objects.filter(artist_id=get_id)
            for item in data_album:
                data_serialized = AlbumSerializer(item)

                dict_aux = dict(data_serialized.data)
                dict_data = dict()

                dict_data["id"] = item.id
                #print("1")
                dict_data["artist_id"] = item.artist_id_id
                #print("2")
                #name genre
                dict_data["name"] = dict_aux["name"]
                dict_data["genre"] = dict_aux["genre"]

                dict_data["artist"] = item.artist
                #print("3")
                dict_data["tracks"] = item.tracks
                #print("4")
                dict_data["self"] = f"https://t2integracion.herokuapp.com/albums/{item.id}"
                #print("5")
                
                list_aux.append(dict_data)
            # en la list_aux tenemos el json con todos los album

            list_aux2 = []
            for a in list_aux:
                aux_id_album = a["id"]
                data_tracks = Track.objects.filter(album_id=aux_id_album) #saco las canciones del album a

                for item in data_tracks:

                    data_serialized = TrackSerializer(item)

                    dict_aux = dict(data_serialized.data)
                    dict_data = dict()

                    dict_data["id"] = item.id
                    #print("1")
                    dict_data["album_id"] = item.album_id_id
                    #print("2")
                    #name genre
                    dict_data["name"] = dict_aux["name"]
                    dict_data["duration"] = dict_aux["duration"]

                    dict_data["times_played"] = item.times_played
                    #print("3")
                    dict_data["artist"] = item.artist
                    #print("4")
                    dict_data["album"] = item.album

                    dict_data["self"] = f"https://t2integracion.herokuapp.com/albums/{item.id}"
                    #print("5")
                    list_aux2.append(dict_data)


            return Response(list_aux2,status=status.HTTP_200_OK)

            '''
            data_album = Album.objects.filter(id=get_id)

            print("pase")
            data_serialized = AlbumSerializer(data_album)
            print("pase2")
            dict_data = dict(data_serialized.data)
            print("pase3")
            dict_data["id"] = data_album.id
            print("pase4")

            return Response(dict_data)
            '''

        except:
            print("entre a error***")

            return Response({})


# ---------

class PlayTrack(APIView):
    serializer_class = serializers.TrackSerializer


    def put(self, request, pk):
        try:
            cancion = Track.objects.get(id=pk)
            cancion.times_played += 1
            cancion.save()
            return Response(status=status.HTTP_200_OK)  
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND) 


class PlayAlbum(APIView):
    serializer_class = serializers.AlbumSerializer

    def put(self, request, pk):
        try:
            album_canciones = Album.objects.get(id=pk)
            canciones = Track.objects.filter(album_id=album_canciones.id)
            for c in canciones:
                c.times_played += 1
                c.save()

            return Response(status=status.HTTP_200_OK)  
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND) 

class PlayArtist(APIView):
    serializer_class = serializers.ArtistSerializer

    def put(self, request, pk):
        try:
            artista = Artist.objects.get(id=pk)
            albums = Album.objects.filter(artist_id=artista.id)
            for a in albums:
                canciones = Track.objects.filter(album_id=a.id)
                for c in canciones:
                    c.times_played += 1
                    c.save()

            return Response(status=status.HTTP_200_OK)  
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND) 




