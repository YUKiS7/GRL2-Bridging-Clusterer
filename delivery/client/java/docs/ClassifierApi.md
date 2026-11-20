# ClassifierApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getClusters**](ClassifierApi.md#getClusters) | **GET** /clusters | Get Clusters |
| [**getClustersWithHttpInfo**](ClassifierApi.md#getClustersWithHttpInfo) | **GET** /clusters | Get Clusters |
| [**getSuspiciousLevels**](ClassifierApi.md#getSuspiciousLevels) | **GET** /suspicious_levels | Get Suspicious Levels |
| [**getSuspiciousLevelsWithHttpInfo**](ClassifierApi.md#getSuspiciousLevelsWithHttpInfo) | **GET** /suspicious_levels | Get Suspicious Levels |
| [**getTechniques**](ClassifierApi.md#getTechniques) | **GET** /techniques | Get Techniques |
| [**getTechniquesWithHttpInfo**](ClassifierApi.md#getTechniquesWithHttpInfo) | **GET** /techniques | Get Techniques |
| [**getVersion**](ClassifierApi.md#getVersion) | **GET** /version | Get Version |
| [**getVersionWithHttpInfo**](ClassifierApi.md#getVersionWithHttpInfo) | **GET** /version | Get Version |
| [**label**](ClassifierApi.md#label) | **POST** /label | Label |
| [**labelWithHttpInfo**](ClassifierApi.md#labelWithHttpInfo) | **POST** /label | Label |



## getClusters

> ClustersResponse getClusters()

Get Clusters

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            ClustersResponse result = apiInstance.getClusters();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getClusters");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ClustersResponse**](ClustersResponse.md)


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

## getClustersWithHttpInfo

> ApiResponse<ClustersResponse> getClustersWithHttpInfo()

Get Clusters

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.ApiResponse;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            ApiResponse<ClustersResponse> response = apiInstance.getClustersWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getClusters");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

ApiResponse<[**ClustersResponse**](ClustersResponse.md)>


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |


## getSuspiciousLevels

> SuspiciousLevelsResponse getSuspiciousLevels()

Get Suspicious Levels

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            SuspiciousLevelsResponse result = apiInstance.getSuspiciousLevels();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getSuspiciousLevels");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**SuspiciousLevelsResponse**](SuspiciousLevelsResponse.md)


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

## getSuspiciousLevelsWithHttpInfo

> ApiResponse<SuspiciousLevelsResponse> getSuspiciousLevelsWithHttpInfo()

Get Suspicious Levels

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.ApiResponse;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            ApiResponse<SuspiciousLevelsResponse> response = apiInstance.getSuspiciousLevelsWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getSuspiciousLevels");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

ApiResponse<[**SuspiciousLevelsResponse**](SuspiciousLevelsResponse.md)>


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |


## getTechniques

> TechniquesResponse getTechniques()

Get Techniques

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            TechniquesResponse result = apiInstance.getTechniques();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getTechniques");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**TechniquesResponse**](TechniquesResponse.md)


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

## getTechniquesWithHttpInfo

> ApiResponse<TechniquesResponse> getTechniquesWithHttpInfo()

Get Techniques

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.ApiResponse;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            ApiResponse<TechniquesResponse> response = apiInstance.getTechniquesWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getTechniques");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

ApiResponse<[**TechniquesResponse**](TechniquesResponse.md)>


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |


## getVersion

> VersionResponse getVersion()

Get Version

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            VersionResponse result = apiInstance.getVersion();
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getVersion");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**VersionResponse**](VersionResponse.md)


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

## getVersionWithHttpInfo

> ApiResponse<VersionResponse> getVersionWithHttpInfo()

Get Version

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.ApiResponse;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        try {
            ApiResponse<VersionResponse> response = apiInstance.getVersionWithHttpInfo();
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#getVersion");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters

This endpoint does not need any parameter.

### Return type

ApiResponse<[**VersionResponse**](VersionResponse.md)>


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |


## label

> LabelResponse label(replay)

Label

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        List<Replay> replay = Arrays.asList(); // List<Replay> | 
        try {
            LabelResponse result = apiInstance.label(replay);
            System.out.println(result);
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#label");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Reason: " + e.getResponseBody());
            System.err.println("Response headers: " + e.getResponseHeaders());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **replay** | [**List&lt;Replay&gt;**](Replay.md)|  | |

### Return type

[**LabelResponse**](LabelResponse.md)


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

## labelWithHttpInfo

> ApiResponse<LabelResponse> labelWithHttpInfo(replay)

Label

### Example

```java
// Import classes:
import grl.client.ApiClient;
import grl.client.ApiException;
import grl.client.ApiResponse;
import grl.client.Configuration;
import grl.client.models.*;
import grl.client.api.ClassifierApi;

public class Example {
    public static void main(String[] args) {
        ApiClient defaultClient = Configuration.getDefaultApiClient();
        defaultClient.setBasePath("http://localhost");

        ClassifierApi apiInstance = new ClassifierApi(defaultClient);
        List<Replay> replay = Arrays.asList(); // List<Replay> | 
        try {
            ApiResponse<LabelResponse> response = apiInstance.labelWithHttpInfo(replay);
            System.out.println("Status code: " + response.getStatusCode());
            System.out.println("Response headers: " + response.getHeaders());
            System.out.println("Response body: " + response.getData());
        } catch (ApiException e) {
            System.err.println("Exception when calling ClassifierApi#label");
            System.err.println("Status code: " + e.getCode());
            System.err.println("Response headers: " + e.getResponseHeaders());
            System.err.println("Reason: " + e.getResponseBody());
            e.printStackTrace();
        }
    }
}
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **replay** | [**List&lt;Replay&gt;**](Replay.md)|  | |

### Return type

ApiResponse<[**LabelResponse**](LabelResponse.md)>


### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

