import asyncio
from typing import Optional
import pytest
import logging

from vultr.apis import *
from vultr.apis.container_registry import list_regions
from vultr.apis.instances import create_instance, get_instance
from vultr.apis.operating_systems import list_os_images
from vultr.apis.plans import list_plans
from vultr.apis.regions import get_available_plans_in_region
from vultr.structs.instance import CreateInstanceData

logger = logging.getLogger(__name__)

async def wait_for_deploy(instance_id: str, timeout: int = 300, interval: int = 5):
    """
    Poll the instance status until it's fully deployed or until timeout.
    
    Args:
        instance_id (str): ID of the newly created instance.
        timeout (int): Maximum wait time in seconds.
        interval (int): Seconds to wait between each poll.

    Raises:
        RuntimeError: If the instance doesn't become ready within the timeout.
    """
    elapsed = 0
    while elapsed < timeout:
        status_info = await get_instance(instance_id)  # API 호출 또는 함수 구현 필요
        # 예: response.get("instance").get("status") == "complete"
        if status_info.get("status") == "complete":
            return
        await asyncio.sleep(interval)
        elapsed += interval

    raise RuntimeError(f"Instance {instance_id} did not become 'complete' within {timeout} seconds.")


# @pytest.mark.asyncio
# async def test_list_regions(api_key):
# 	try:
# 		result = await list_regions()

# 		if result.get("status") != 200:
# 			raise Exception(result)
		
# 		logger.info("\nResponse Data:\n%s", result)

# 	except Exception as e:
# 		logger.error("Error: %s", e)
# 		pytest.fail(f"Test failed with error: {e}")

# @pytest.mark.asyncio
# async def test_get_available_plans_in_region(api_key):
# 	try:
# 		result = await get_available_plans_in_region(region_id="ewr", type="vc2")

# 		if result.get("status") != 200:
# 			raise Exception(result)
		
# 		logger.info("\nResponse Data:\n%s", result)

# 	except Exception as e:
# 		logger.error("Error: %s", e)
# 		pytest.fail(f"Test failed with error: {e}")

# @pytest.mark.asyncio
# async def test_list_os_images(api_key):
# 	try:
# 		result = await list_os_images(per_page=10, cursor="bmV4dF9fMjA3Nw==")

# 		if result.get("status") != 200:
# 			raise Exception(result)
		
# 		logger.info("\nResponse Data:\n%s", result)

# 	except Exception as e:
# 		logger.error("Error: %s", e)
# 		pytest.fail(f"Test failed with error: {e}")

instance_id: Optional[str] = None

@pytest.mark.asyncio
async def test_create_instance(api_key):
	try:
		data = CreateInstanceData(region="ewr", plan="vc2-1c-0.5gb-v6")\
			.os_id(2136)\
			.hostname("testhostname")\
			.label("test_label")\
			.ddos_protection(False)\
			.backups("disabled")\

		result = await create_instance(data)

		if result.get("status") != 202:
			raise Exception(result)
		
		logger.info("\nResponse Data:\n%s", result)

		global instance_id
		instance_id = result.get("instance").get("id")

		print(instance_id)
	except Exception as e:
		logger.error("Error: %s", e)
		pytest.fail(f"Test failed with error: {e}")

# @pytest.mark.asyncio
# async def test_