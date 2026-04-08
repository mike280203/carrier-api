"""Test der find_by_id Methode."""
from carrier.entity.carrier import Carrier
from carrier.entity.carrier_type import CarrierType
from carrier.entity.commandcenter import CommandCenter
from carrier.repository.carrier_repository import CarrierRepository
from carrier.repository.session_factory import Session


def main() -> None:
    """Test der find_by_id Methode."""
    session = Session()
    repo = CarrierRepository()
    test_carrier_id: int | None = None

    try:
        test_commandcenter = CommandCenter(
            id=None,
            code_name="Test Command Center",
            security_level=3,
            carrier_id=None,
            carrier=None,
        )

        test_carrier = Carrier(
            id=None,
            name="Test Carrier",
            nation="United States",
            carrier_type=CarrierType.AIRCRAFT_CARRIER,
            commandcenter=test_commandcenter,
            aircrafts=[],
        )

        session.add(test_carrier)
        session.commit()
        session.refresh(test_carrier)

        test_carrier_id = test_carrier.id
        print(f"Gespeicherte ID: {test_carrier_id}")

        found = repo.find_by_id(test_carrier_id, session)
        print(f"Gefunden: {found}")
        print(f"CommandCenter: {found.commandcenter if found else None}")

    finally:
        if test_carrier_id is not None:
            carrier_to_delete = session.get(Carrier, test_carrier_id)
            if carrier_to_delete is not None:
                session.delete(carrier_to_delete)
                session.commit()
                print(f"Test-Datensatz mit ID {test_carrier_id} wieder geloescht.")

        session.close()


if __name__ == "__main__":
    main()
