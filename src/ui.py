from varasto import Varasto


class VarastoUI:
    def __init__(self):
        self.varastot = {}
        self.seuraava_id = 1

    def nayta_menu(self):
        print("\n" + "="*50)
        print("VARASTO HALLINTAJÄRJESTELMÄ")
        print("="*50)
        print("1. Luo uusi varasto")
        print("2. Näytä kaikki varastot")
        print("3. Lisää tavaraa varastoon")
        print("4. Ota tavaraa varastosta")
        print("5. Näytä varasto tiedot")
        print("6. Poista varasto")
        print("0. Lopeta")
        print("-"*50)

    def luo_varasto(self):
        print("\nLuodaan uusi varasto:")
        try:
            nimi = input("Anna varastolle nimi: ").strip()
            if not nimi:
                print("Nimi ei voi olla tyhjä!")
                return

            if nimi in [v['nimi'] for v in self.varastot.values()]:
                print("Varasto tällä nimellä on jo olemassa!")
                return

            tilavuus = float(input("Anna varaston tilavuus: "))
            alku_saldo = input("Anna alkusaldo (Enter = 0): ").strip()
            alku_saldo = float(alku_saldo) if alku_saldo else 0.0

            varasto = Varasto(tilavuus, alku_saldo)
            varasto_id = self.seuraava_id
            self.varastot[varasto_id] = {
                'nimi': nimi,
                'varasto': varasto
            }
            self.seuraava_id += 1

            print(f"Varasto '{nimi}' luotu onnistuneesti! (ID: {varasto_id})")
            print(f"Varasto: {varasto}")

        except ValueError:
            print("Virhe: Anna numerot oikeassa muodossa!")
        except Exception as e:
            print(f"Virhe luotaessa varastoa: {e}")

    def nayta_varastot(self):
        if not self.varastot:
            print("\nEi varastoja.")
            return

        print("\nKaikki varastot:")
        print("-"*60)
        for varasto_id, data in self.varastot.items():
            nimi = data['nimi']
            varasto = data['varasto']
            print(f"ID: {varasto_id} | Nimi: {nimi}")
            print(f"    {varasto}")
            print("-"*60)

    def valitse_varasto(self, toiminto):
        if not self.varastot:
            print("\nEi varastoja. Luo ensin varasto!")
            return None

        print(f"\nValitse varasto ({toiminto}):")
        for varasto_id, data in self.varastot.items():
            print(f"{varasto_id}. {data['nimi']} - {data['varasto']}")

        try:
            valinta = int(input("Anna varaston ID: "))
            if valinta in self.varastot:
                return valinta
            else:
                print("Virheellinen varaston ID!")
                return None
        except ValueError:
            print("Anna numero!")
            return None

    def lisaa_tavaraa(self):
        varasto_id = self.valitse_varasto("lisäys")
        if varasto_id is None:
            return

        try:
            maara = float(input("Kuinka paljon lisätään: "))
            varasto = self.varastot[varasto_id]['varasto']
            nimi = self.varastot[varasto_id]['nimi']
            
            print(f"\nEnnen lisäystä: {varasto}")
            varasto.lisaa_varastoon(maara)
            print(f"Lisäys suoritettu varastoon '{nimi}'")
            print(f"Lisäyksen jälkeen: {varasto}")

        except ValueError:
            print("Anna numero!")

    def ota_tavaraa(self):
        varasto_id = self.valitse_varasto("otto")
        if varasto_id is None:
            return

        try:
            maara = float(input("Kuinka paljon otetaan: "))
            varasto = self.varastot[varasto_id]['varasto']
            nimi = self.varastot[varasto_id]['nimi']
            
            print(f"\nEnnen ottoa: {varasto}")
            saatu = varasto.ota_varastosta(maara)
            print(f"Otettiin {saatu} varastosta '{nimi}'")
            print(f"Oton jälkeen: {varasto}")

        except ValueError:
            print("Anna numero!")

    def nayta_varasto_tiedot(self):
        varasto_id = self.valitse_varasto("tarkastelu")
        if varasto_id is None:
            return

        data = self.varastot[varasto_id]
        nimi = data['nimi']
        varasto = data['varasto']
        
        print(f"\nVarasto '{nimi}' (ID: {varasto_id}):")
        print(f"Tilavuus: {varasto.tilavuus}")
        print(f"Saldo: {varasto.saldo}")
        print(f"Vapaata tilaa: {varasto.paljonko_mahtuu()}")
        print(f"Täyttöaste: {(varasto.saldo / varasto.tilavuus * 100):.1f}%")

    def poista_varasto(self):
        varasto_id = self.valitse_varasto("poisto")
        if varasto_id is None:
            return

        nimi = self.varastot[varasto_id]['nimi']
        vahvistus = input(f"Haluatko varmasti poistaa varaston '{nimi}'? (k/e): ").lower()
        
        if vahvistus == 'k':
            del self.varastot[varasto_id]
            print(f"Varasto '{nimi}' poistettu!")
        else:
            print("Poisto peruttu.")

    def suorita(self):
        print("Tervetuloa varasto hallintajärjestelmään!")
        
        while True:
            self.nayta_menu()
            
            try:
                valinta = input("Valitse toiminto (0-6): ").strip()
                
                if valinta == '0':
                    print("Kiitos ohjelman käytöstä!")
                    break
                elif valinta == '1':
                    self.luo_varasto()
                elif valinta == '2':
                    self.nayta_varastot()
                elif valinta == '3':
                    self.lisaa_tavaraa()
                elif valinta == '4':
                    self.ota_tavaraa()
                elif valinta == '5':
                    self.nayta_varasto_tiedot()
                elif valinta == '6':
                    self.poista_varasto()
                else:
                    print("Virheellinen valinta! Anna numero 0-6.")
                    
            except KeyboardInterrupt:
                print("\n\nOhjelma keskeytetty. Näkemiin!")
                break
            except Exception as e:
                print(f"Odottamaton virhe: {e}")

            input("\nPaina Enter jatkaaksesi...")


def main():
    ui = VarastoUI()
    ui.suorita()


if __name__ == "__main__":
    main()